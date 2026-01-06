from logger import logger
import json
import os

USE_MUSICGEN = True  # True = IA | False = mock

print(f"DEBUG: USE_MUSICGEN = {USE_MUSICGEN}")
print(f"DEBUG: Current directory: {os.getcwd()}")

if USE_MUSICGEN:
    from agents.music_agent_musicgen import MusicAgent
    print("DEBUG: Loading music_agent_musicgen.py (REAL API)")
else:
    from agents.teste_mock import MusicAgent  # Alterado aqui!
    print("DEBUG: Loading teste_mock.py (MOCK)")

from agents.marketing_agent import MarketingAgent

def run():
    logger.info("Pipeline started")
    
    config_file = "storage/last_config.json"
    
    if os.path.exists(config_file):
        with open(config_file, "r") as f:
            config = json.load(f)
        
        mode = config.get("mode", "guided")
        params = config.get("params", {})
        prompt = config.get("prompt", "")
        
        # DEBUG: Verificar se duration está chegando
        print(f"DEBUG: mode={mode}, params={params}")
        print(f"DEBUG: duration param = {params.get('duration', 'NOT FOUND')}")
        
        prompt_preview = prompt[:50] + "..." if prompt and len(prompt) > 50 else (prompt or "")
        logger.info(f"Mode: {mode}, Params: {params}, Prompt: {prompt_preview}")
        
        # Garantir que duration está presente nos params
        if "duration" not in params:
            params["duration"] = 5
            print(f"DEBUG: Added default duration: {params['duration']}")
        
        music = MusicAgent(mode=mode, params=params, prompt=prompt).run()
    else:
        logger.warning("Config file not found, using default")
        music = MusicAgent().run()
    
    logger.info(f"Music generated: {music}")
    
    MarketingAgent().run(music)
    logger.info("Teaser published")
    
    logger.info("Pipeline finished")
    return {"success": True, "audio_file": music}

if __name__ == "__main__":
    run()