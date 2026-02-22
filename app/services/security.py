"""
Serviços de Segurança e Autenticação

Arquivo responsável por:
- Hashing e verificação de senhas
- Criação e validação de tokens JWT
- Extração e validação de tokens de requisições

Autor: Seu Nome
"""

from datetime import datetime, timedelta  # Manipulação de datas e horas
from typing import Optional  # Type hints para valores opcionais
from fastapi import Depends, HTTPException, status  # FastAPI utilities
from fastapi.security import OAuth2PasswordBearer  # Esquema OAuth2 para Bearer tokens
from jose import jwt, JWTError  # Criação e decodificação de JWT
from passlib.context import CryptContext  # Contexto para hashing de senhas
from app.config import settings  # Configurações da aplicação

# ============ CONFIGURAÇÃO DE CRIPTOGRAFIA ============
# Contexto CryptContext para gerenciar hashing de senhas
# schemes: lista de algoritmos suportados (bcrypt é o mais seguro)
# deprecated: algoritmos antigos que funcionam mas não são mais recomendados
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Esquema de autenticação OAuth2
# tokenUrl: endpoint onde o cliente faz login para obter o token
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="fornecedores/login")

# ============ FUNÇÕES DE HASH DE SENHA ============

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    Verifica se a senha em texto plano corresponde ao hash armazenado.
    
    Parâmetros:
        plain_password (str): Senha fornecida pelo usuário
        hashed_password (str): Hash da senha armazenada no banco
    
    Retorna:
        bool: True se as senhas coincidem, False caso contrário
    """
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password: str) -> str:
    """
    Gera o hash bcrypt de uma senha.
    
    Parâmetros:
        password (str): Senha em texto plano
    
    Retorna:
        str: Hash bcrypt da senha (seguro para armazenar em banco de dados)
    """
    return pwd_context.hash(password)

# ============ FUNÇÕES DE TOKEN JWT ============

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    """
    Cria um token JWT com os dados fornecidos.
    
    Parâmetros:
        data (dict): Payload do token (dados a codificar)
                     Exemplo: {"sub": "email@example.com", "role": "restaurante"}
        expires_delta (Optional[timedelta]): Tempo de expiração customizado
                                             Se None, usa valor padrão de settings
    
    Retorna:
        str: Token JWT codificado
    
    Exemplo:
        token = create_access_token({"sub": "user@email.com"})
    """
    # Cria uma cópia dos dados para não modificar o original
    to_encode = data.copy()
    
    # Define o tempo de expiração do token
    if expires_delta:
        # Se foi fornecido um tempo customizado, o utiliza
        expire = datetime.utcnow() + expires_delta
    else:
        # Caso contrário, usa o tempo padrão de settings (ex: 30 minutos)
        expire = datetime.utcnow() + timedelta(minutes=settings.access_token_expire_minutes)
    
    # Adiciona a data de expiração ao payload
    to_encode.update({"exp": expire})
    
    # Codifica o token usando a chave secreta e algoritmo HS256
    # jwt.encode é da biblioteca python-jose
    encoded_jwt = jwt.encode(to_encode, settings.secret_key, algorithm=settings.algorithm)
    
    return encoded_jwt

# ============ FUNÇÕES DE VALIDAÇÃO DE TOKEN ============

def get_current_user_email(token: str = Depends(oauth2_scheme)) -> str:
    """
    Extrai e valida o email do usuário a partir do token JWT.
    Esta função é usada como dependência em rotas protegidas.
    
    Parâmetros:
        token (str): Token JWT extraído do header Authorization
                     Formato: "Authorization: Bearer {token}"
    
    Retorna:
        str: Email do usuário autenticado
    
    Levanta:
        HTTPException: Se o token é inválido ou expirado
    
    Exemplo de uso em uma rota:
        @router.get("/perfil")
        def get_perfil(email: str = Depends(get_current_user_email)):
            # email contém o email do usuário autenticado
            return {"email": email}
    """
    # Exceção padrão para erro de autenticação
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,  # 401 = Não autorizado
        detail="Não foi possível validar as credenciais",  # Mensagem de erro
        headers={"WWW-Authenticate": "Bearer"},  # Headers padrão do OAuth2
    )
    
    try:
        # Decodifica o token JWT usando a chave secreta
        payload = jwt.decode(token, settings.secret_key, algorithms=[settings.algorithm])
        
        # Extrai o email do payload (armazenado na chave "sub")
        email: str = payload.get("sub")
        
        # Se o email não existe no token, lança exceção
        if email is None:
            raise credentials_exception
        
        # Retorna o email do usuário autenticado
        return email
    
    except JWTError:
        # Se houver erro ao decodificar o token (expirado, inválido, etc)
        raise credentials_exception