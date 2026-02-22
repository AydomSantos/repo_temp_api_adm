"""
Configurações Centralizadas da Aplicação

Arquivo responsável por centralizar todas as configurações do projeto.
Evita valores sensíveis espalhados pelo código.
Utiliza variáveis de ambiente para maior segurança.

Autor: Seu Nome
"""

import os  # Acesso a variáveis de ambiente
from pathlib import Path  # Manipulação de caminhos de arquivos
from pydantic import BaseModel  # Validação de dados com Pydantic

# Obtém o diretório raiz do projeto (um nível acima do app/)
BACK_ROOT = Path(__file__).resolve().parents[1]

# Tenta carregar variáveis de ambiente do arquivo .env
try:
    from dotenv import load_dotenv  # Biblioteca para carregar arquivo .env
    env_path = BACK_ROOT / ".env"  # Caminho para o arquivo .env
    # Carrega as variáveis de ambiente se o arquivo existir
    load_dotenv(env_path)
except ImportError:
    # Se python-dotenv não estiver instalado, exibe aviso
    print("Alerta: python-dotenv não instalado. Variáveis de ambiente não serão carregadas.")

# Classe de configurações usando Pydantic
# Valida e gerencia todos os valores de configuração
class Settings(BaseModel):
    # ============ SEGURANÇA ============
    # Chave secreta para assinar tokens JWT (MUDE EM PRODUÇÃO!)
    secret_key: str = os.getenv("SECRET_KEY", "CHANGE_ME_SUPER_KEY_FOR_CLASSROOM")
    
    # Chave da API Stripe para processamento de pagamentos (modo teste)
    stripe_api_key: str = os.getenv("STRIPE_API_KEY", "sk_test_placeholder")

    # ============ TOKENS JWT ============
    # Algoritmo de assinatura para os tokens JWT (HS256 = HMAC SHA256)
    algorithm: str = "HS256"

    # Tempo de expiração dos tokens em minutos (TTL - Time To Live)
    access_token_expire_minutes: int = 30

    # ============ BANCO DE DADOS ============
    # Caminho para o arquivo JSON do banco TinyDB
    database_path: str = str(BACK_ROOT / "data" / "database.json")

    # ============ DEBUG/DESENVOLVIMENTO ============
    # Se True, retorna o token de reset em respostas para facilitar testes
    debug_password_reset_token: bool = True

# Instancia única das configurações (padrão Singleton)
# Use em toda a aplicação: from app.config import settings
settings = Settings()
