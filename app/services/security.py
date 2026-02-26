"""
Funcoes de seguranca da API.

Responsavel por:
- hash e validacao de senha
- criacao e leitura de JWT
- controle simples de autorizacao por papel (role)
"""

from datetime import datetime, timedelta, timezone
from typing import Optional

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from passlib.context import CryptContext

from app.config import settings

# Contexto de hash de senha com bcrypt.
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
# Define de qual endpoint o Swagger obtira token.
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Compara senha em texto puro com hash salvo."""
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password: str) -> str:
    """Gera hash seguro para persistir senha no banco."""
    return pwd_context.hash(password)


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    """Cria token JWT com payload e tempo de expiracao."""
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + (
        expires_delta or timedelta(minutes=settings.access_token_expire_minutes)
    )
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, settings.secret_key, algorithm=settings.algorithm)


def get_current_user_email(token: str = Depends(oauth2_scheme)) -> str:
    """Extrai email (claim sub) de um token valido."""
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Nao foi possivel validar as credenciais",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        payload = jwt.decode(token, settings.secret_key, algorithms=[settings.algorithm])
        email: str | None = payload.get("sub")
        if not email:
            raise credentials_exception
        return email
    except JWTError:
        raise credentials_exception


def get_current_user_payload(token: str = Depends(oauth2_scheme)) -> dict:
    """Retorna payload completo do JWT para regras de autorizacao."""
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Nao foi possivel validar as credenciais",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, settings.secret_key, algorithms=[settings.algorithm])
        if not payload.get("sub"):
            raise credentials_exception
        return payload
    except JWTError:
        raise credentials_exception


def require_role(expected_role: str):
    """
    Fabrica de dependencia para restringir endpoint por papel.

    Exemplo:
    Depends(require_role("fornecedor"))
    """

    def role_dependency(payload: dict = Depends(get_current_user_payload)) -> str:
        if payload.get("role") != expected_role:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Permissao insuficiente para acessar este recurso.",
            )
        # Retorna email autenticado para o endpoint consumir.
        return payload["sub"]

    return role_dependency
