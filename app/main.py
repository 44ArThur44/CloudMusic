from flask import Flask, render_template, send_file, request, jsonify
import sys
import subprocess
import os
import json
from agents.billing_agent import BillingAgent
import stripe
from dotenv import load_dotenv
import hashlib

# Carregar variáveis de ambiente
load_dotenv()

# Configurar Stripe
stripe.api_key = os.getenv("STRIPE_SECRET_KEY")

# Inicializar Flask
app = Flask(__name__)

# Configurações de diretório
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
STORAGE_DIR = os.path.join(BASE_DIR, "storage")
os.makedirs(STORAGE_DIR, exist_ok=True)

# Inicializar billing agent
billing = BillingAgent()


def get_client_id():
    """Gera ID único baseado em IP + User-Agent"""
    ip = request.remote_addr
    user_agent = request.headers.get('User-Agent', '')
    unique_string = f"{ip}|{user_agent}"
    return hashlib.md5(unique_string.encode()).hexdigest()


def get_user_id():
    """Helper para pegar user_id do request"""
    return request.json.get('user_id') if request.json else 'default_user'


# ==================== ROTAS PÚBLICAS ====================

@app.route("/")
def index():
    """Página principal"""
    return render_template("index.html")


@app.route("/music/<filename>")
def music(filename):
    """Serve arquivo de áudio"""
    path = os.path.join(STORAGE_DIR, filename)
    if os.path.exists(path):
        response = send_file(path, mimetype="audio/wav")
        
        # Adicionar headers para streaming adequado
        response.headers['Accept-Ranges'] = 'bytes'
        response.headers['Cache-Control'] = 'no-cache'
        
        # Obter tamanho do arquivo
        file_size = os.path.getsize(path)
        response.headers['Content-Length'] = file_size
        
        return response
    return jsonify({"error": "File not found"}), 404


@app.route("/download/<filename>")
def download(filename):
    """Download de arquivo de áudio"""
    path = os.path.join(STORAGE_DIR, filename)
    if os.path.exists(path):
        return send_file(path, as_attachment=True)
    return jsonify({"error": "File not found"}), 404


@app.route("/success")
def success():
    """Página de sucesso após pagamento"""
    return """
    <h1>Pagamento Concluído!</h1>
    <p>Seus créditos foram adicionados à sua conta.</p>
    <p><a href="/">Voltar ao CloudMusic</a></p>
    """


@app.route("/cancel")
def cancel():
    """Página de cancelamento de pagamento"""
    return """
    <h1>Pagamento Cancelado</h1>
    <p>Nenhum crédito foi adicionado.</p>
    <p><a href="/">Voltar ao CloudMusic</a></p>
    """

# ==================== ROTAS DE API ====================

@app.route("/check-limit", methods=["POST"])
def check_limit():
    """Verifica limite disponível do usuário"""
    try:
        user_id = get_client_id()
        result = billing.run(user_id, "check")
        
        if result["allowed"]:
            return jsonify({
                "allowed": True,
                "remaining": result.get("remaining_free", 0),
                "credits": result.get("remaining_credits", 0)
            })
        else:
            return jsonify({
                "allowed": False,
                "message": "Daily limit reached",
                "remaining_time": "24h",
                "remaining": 0
            })
    except Exception as e:
        return jsonify({"allowed": False, "error": str(e)}), 500


@app.route("/generate", methods=["POST"])
def generate():
    """Rota principal de geração de música"""
    try:
        data = request.json
        print(f"DADOS recebidos: {data}")  
        
        # 1. VERIFICAR E CONSUMIR LIMITE
        user_id = get_client_id()
        billing_result = billing.run(user_id, "consume")
        
        if not billing_result["allowed"]:
            return jsonify({
                "success": False,
                "error": "Daily limit reached. Please wait 24h or buy credits."
            }), 403
        
        # 2. Preparar dados para o pipeline
        mode = data.get('mode', 'guided')
        
        # Salvar configuração EM CORRETO
        config_data = {
            "mode": data.get('mode', 'guided'),
            "params": data.get('params', {}),  # I duration
            "prompt": data.get('prompt', '')
        }
        
        config_file = os.path.join(STORAGE_DIR, "last_config.json")
        with open(config_file, "w") as f:
            json.dump(config_data, f, indent=2)
        
        print(f"CONFIG salva: {config_data}") 
        
        # 3. Executar pipeline
        print(f"EXECUTANDO pipeline no modo: {mode}")  
        result = subprocess.run(
            [sys.executable, "run_pipeline.py"],
            capture_output=True,
            text=True,
            cwd=BASE_DIR
        )
        
        # 4. Verificar resultado
        if result.returncode != 0:
            print(f"ERRO no pipeline: {result.stderr}")  
            return jsonify({
                "success": False, 
                "error": f"Pipeline failed: {result.stderr[:200]}"
            }), 500
        
        # 5. Encontrar arquivo mais recente no storage
        wav_files = [f for f in os.listdir(STORAGE_DIR) if f.endswith('.wav')]
        if not wav_files:
            return jsonify({
                "success": False,
                "error": "No audio file generated"
            }), 500
        
        # Pega o mais recente
        wav_files.sort(key=lambda x: os.path.getmtime(os.path.join(STORAGE_DIR, x)), reverse=True)
        latest_file = wav_files[0]
        
        return jsonify({
            "success": True,
            "audio_file": latest_file,
            "filename": latest_file,  # Mantém compatibilidade
            "prompt_used": data.get('prompt', ''),
            "billing": {
                "mode": billing_result.get("mode", "free"),
                "remaining": billing_result.get("remaining_free", 0),
                "credits": billing_result.get("remaining_credits", 0)
            }
        })
        
    except Exception as e:
        print(f"ERRO em /generate: {str(e)}")  # DEBUG - Em vez de ❌
        return jsonify({"success": False, "error": str(e)}), 500


@app.route("/add-credits", methods=["POST"])
def add_credits():
    """Rota mock para adicionar créditos (testes)"""
    try:
        data = request.json
        user_id = data.get("user_id", get_client_id())
        amount = data.get("amount", 10)

        billing.add_credits(user_id, amount)
        return jsonify({"success": True, "credits_added": amount})
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500


@app.route("/create-checkout-session", methods=["POST"])
def create_checkout_session():
    """Cria sessão de checkout do Stripe"""
    try:
        user_id = get_client_id()
        
        # Verifica se está em desenvolvimento
        if os.getenv("FLASK_ENV") == "development":
            domain = "http://localhost:5000"
        else:
            domain = "https://seusite.com"
        
        session = stripe.checkout.Session.create(
            payment_method_types=["card"],
            mode="payment",
            client_reference_id=user_id,
            line_items=[{
                "price_data": {
                    "currency": "usd",
                    "product_data": {
                        "name": "40 Credits - CloudMusic",
                        "description": "Generate 40 AI music loops"
                    },
                    "unit_amount": 400  # $4.00
                },
                "quantity": 1
            }],
            success_url=f"{domain}/success?session_id={{CHECKOUT_SESSION_ID}}",
            cancel_url=f"{domain}/cancel",
            metadata={"user_id": user_id, "credits": "40"}
        )

        return jsonify({"url": session.url})
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/webhook/stripe", methods=["POST"])
def stripe_webhook():
    """Webhook do Stripe para processar pagamentos"""
    payload = request.data
    sig_header = request.headers.get("Stripe-Signature")
    webhook_secret = os.getenv("STRIPE_WEBHOOK_SECRET")

    if not webhook_secret:
        print("AVISO: STRIPE_WEBHOOK_SECRET não configurado")
        return jsonify({"error": "Webhook secret not configured"}), 400

    try:
        event = stripe.Webhook.construct_event(
            payload, sig_header, webhook_secret
        )
    except ValueError:
        return jsonify({"error": "Invalid payload"}), 400
    except stripe.error.SignatureVerificationError:
        return jsonify({"error": "Invalid signature"}), 400

    # Processar evento
    if event["type"] == "checkout.session.completed":
        session = event["data"]["object"]
        user_id = session.get("client_reference_id")
        credits = 40  # Default para a oferta atual
        
        # Adicionar créditos ao usuário
        billing.add_credits(user_id, credits)
        print(f"CREDITOS adicionados: {user_id} +{credits}")  # DEBUG - Em vez de ✅
        
    elif event["type"] == "payment_intent.succeeded":
        print("PAGAMENTO processado com sucesso")  # DEBUG - Em vez de 💳
    
    return jsonify({"status": "ok"})


# ==================== ROTAS DE DEBUG ====================

@app.route("/debug/files")
def debug_files():
    """Lista arquivos no storage (apenas debug)"""
    files = os.listdir(STORAGE_DIR)
    return jsonify({"files": files, "count": len(files)})


# ==================== INICIALIZAÇÃO ====================

if __name__ == "__main__":
    port = int(os.getenv("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=True)