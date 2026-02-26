"""
Configuracoes centralizadas da aplicacao.

Le variaveis de ambiente e concentra os valores usados por toda a API.
"""

import os
from pathlib import Path

from pydantic import BaseModel

# Caminho da raiz do projeto (pasta acima de app/).
BACK_ROOT = Path(__file__).resolve().parents[1]

# Tenta carregar variaveis de ambiente do arquivo .env.
try:
    from dotenv import load_dotenv

    env_path = BACK_ROOT / ".env"
    load_dotenv(env_path)
except ImportError:
    # Se python-dotenv nao estiver instalado, segue com variaveis do sistema.
    pass


class Settings(BaseModel):
    # Chave usada para assinar e validar JWT.
    secret_key: str = os.getenv("SECRET_KEY", "CHANGE_ME_IN_PRODUCTION_MIN_32_CHARS")
    # Chave secreta da Stripe para criar checkout no backend.
    stripe_api_key: str = os.getenv("STRIPE_API_KEY", "sk_test_placeholder")
    # Algoritmo de assinatura do token.
    algorithm: str = "HS256"
    # Tempo de expiracao dos tokens de acesso.
    access_token_expire_minutes: int = 30
    # Caminho do arquivo JSON usado pelo TinyDB.
    database_path: str = str(BACK_ROOT / "data" / "database.json")
    # Em desenvolvimento pode expor token de reset na resposta.
    debug_password_reset_token: bool = os.getenv("DEBUG_PASSWORD_RESET_TOKEN", "false").lower() == "true"


# Instancia unica de configuracao usada no projeto.
settings = Settings()
