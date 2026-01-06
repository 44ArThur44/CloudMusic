import json
import os
from datetime import date

FREE_DAILY_LIMIT = 4

class BillingAgent:
    def __init__(self, db_path="data/billing_db.json"):
        self.db_path = db_path
        if not os.path.exists(self.db_path):
            with open(self.db_path, "w") as f:
                json.dump({}, f)
    def run(self, user_id: str, action: str) -> dict:
        print(f"[Billing] Action: {action} for {user_id}")

        today = date.today().isoformat()

        with open(self.db_path, "r") as f:
            db = json.load(f)

        user = db.get(user_id, {
            "free_usage": 0,
            "credits": 0,
            "last_reset": today
        })

        # reset diário do free
        if user["last_reset"] != today:
            user["free_usage"] = 0
            user["last_reset"] = today
            db[user_id] = user
            self._save(db)

        if action == "check":
            # SÓ VERIFICA, não consome
            return self._check_only(user)
        elif action == "consume":
            # CONSOME crédito/free
            return self._consume_access(user, user_id, db)
        else:
            return {"allowed": False, "error": "Unknown action"}

    def _check_only(self, user: dict) -> dict:
        """Apenas verifica se pode gerar"""
        if user["credits"] > 0:
            return {
                "allowed": True,
                "mode": "paid",
                "remaining_credits": user["credits"]
            }
        
        if user["free_usage"] < FREE_DAILY_LIMIT:
            return {
                "allowed": True,
                "mode": "free",
                "remaining_free": FREE_DAILY_LIMIT - user["free_usage"]
            }
        
        return {
            "allowed": False,
            "action": "block",
            "reason": "Free limit reached. Please purchase credits."
        }

    def _consume_access(self, user: dict, user_id: str, db: dict) -> dict:
        """Consome um acesso (credits ou free)"""
        # usa créditos pagos primeiro
        if user["credits"] > 0:
            user["credits"] -= 1
            db[user_id] = user
            self._save(db)
            return {
                "allowed": True,
                "action": "continue",
                "mode": "paid",
                "remaining_credits": user["credits"]
            }

        # usa free diário
        if user["free_usage"] < FREE_DAILY_LIMIT:
            user["free_usage"] += 1
            db[user_id] = user
            self._save(db)
            return {
                "allowed": True,
                "action": "continue",
                "mode": "free",
                "remaining_free": FREE_DAILY_LIMIT - user["free_usage"]
            }

        # bloqueado
        return {
            "allowed": False,
            "action": "block",
            "reason": "Free limit reached. Please purchase credits."
        }

        # reset diário do free
        if user["last_reset"] != today:
            user["free_usage"] = 0
            user["last_reset"] = today

        # usa créditos pagos primeiro
        if user["credits"] > 0:
            user["credits"] -= 1
            db[user_id] = user
            self._save(db)
            return {
                "allowed": True,
                "action": "continue",
                "mode": "paid",
                "remaining_credits": user["credits"]
            }

        # usa free diário
        if user["free_usage"] < FREE_DAILY_LIMIT:
            user["free_usage"] += 1
            db[user_id] = user
            self._save(db)
            return {
                "allowed": True,
                "action": "continue",
                "mode": "free",
                "remaining_free": FREE_DAILY_LIMIT - user["free_usage"]
            }

        # bloqueado → pedir pagamento
        return {
            "allowed": False,
            "action": "block",
            "reason": "Free limit reached. Please purchase credits."
        }

    def add_credits(self, user_id: str, amount: int):
        with open(self.db_path, "r") as f:
            db = json.load(f)

        user = db.get(user_id, {
            "free_usage": 0,
            "credits": 0,
            "last_reset": date.today().isoformat()
        })

        user["credits"] += amount
        db[user_id] = user
        self._save(db)

    def _save(self, db: dict):
        with open(self.db_path, "w") as f:
            json.dump(db, f, indent=2)
