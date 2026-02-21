"""
Configurações Gerais do Projeto
- Este arquivo concentra valores de ambiente para evitar valores sensiveis espalhados no codigo
"""

import os
from pathlib import Path
from pydantic import BaseModel
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass

# diretorio raiz do backend
BACK_ROOT = Path(__file__).resolve().parents[1]

class Settings(BaseModel):
    secret_key: str = os.getenv("SECRET_KEY", "CHANGE_ME_SUPER_KEY_FOR_CLASSROOM")
    stripe_api_key: str = os.getenv("STRIPE_API_KEY", "sk_test_placeholder")

    # Algoritimo de assinatura do token
    algorithm : str = "HS256"

    # Tempo de expiração do token em minutos
    access_token_expire_minutes: int = 30

    #Arquivo JSON do TinyDB
    database_path: str = str(BACK_ROOT / "data" / "database.json")

    debug_password_reset_token : bool = True

settings = Settings()
