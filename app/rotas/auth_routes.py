"""
Rotas Publicas de autenticação

Todas as Regras de negocio estarão aqui.
"""

import secrets
from fastapi import APIRouter, HTTPException, status

from app.config import settings
from app.models.auth import (
    RegisterUser,
    LoginRequest,
    ForgotPasswordRequest,
    TokenResponse,
    MensageResponse,
    ForgotPasswordResponse,
    ResetPasswordRequest,
    HomeResponse,
)

from app.services.database import (
    find_user_by_email,
    find_user_reset_token,
    insert_user,
    update_user,
)

from app.services.security import create_access_token, get_password_hash, verify_password

router = APIRouter(prefix="/auth", tags=["auth"])

# função Responsavel pela Criação do usuario
@router.post("/register", response_model=MensageResponse)
def register_user(data: RegisterUser):
    # Verifica se senha e confirmação de senha são iguais
    if data.senha != data.confirma_senha:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Senha e Confirma senha não conferem.",
        )
    
    # Verifica se email já está cadastrado
    if find_user_by_email(data.email):
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Email já cadastrado.",
        )

    try:
        insert_user({
            "nome": data.nome.strip(),
            "email": data.email.lower().strip(),
            "senha": get_password_hash(data.senha),
            "reset_token": None,
            "ativo": True,
        })
        return {"mensagem": "Usuário cadastrado com sucesso."}
    except Exception as error:
        # TODO: Adicionar log do erro para depuração
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Ocorreu um erro ao cadastrar o usuário.",
        )
    
# Fução responsavel por fazer o login do usuario
@router.post("/login", response_model=TokenResponse)
def login_user(data: LoginRequest):
    # Verifica se email existe
    user = find_user_by_email(data.email)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Usuário ou senha inválidos.",
        )
    
    # Verifica se senha está correta
    if not verify_password(data.senha, user["senha"]):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Usuário ou senha inválidos.",
        )
    
    # Verifica se usuário está ativo
    if not user.get("ativo", True):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Usuário não está ativo.",
        )

    acess_token = create_access_token(data={"sub": user["email"]})
    return {
        "access_token": acess_token,
        "token_type": "bearer",
    }

# Função responsavel pela parte de esqueçeu a senha 
@router.post("/forgot-password", response_model=ForgotPasswordResponse)
def forgot_password(data: ForgotPasswordRequest):
    user = find_user_by_email(data.email)
    # Por segurança, não informamos se o usuário existe ou está inativo.
    if not user or not user.get("ativo", True):
        return ForgotPasswordResponse(mensagem="Se um usuário com este email existir e estiver ativo, um email de recuperação será enviado.")

    try:
        token = secrets.token_urlsafe(20)
        update_user(user["email"], {"reset_token": token})

        response = {"mensagem": "Email de recuperação enviado."}
        if settings.debug_password_reset_token:
            response["token_debug"] = token
        return ForgotPasswordResponse(**response)
    except Exception as error:
        # TODO: Adicionar log do erro para depuração
        raise HTTPException(
           status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
           detail="Ocorreu um erro ao processar a solicitação.", 
        )

# Função responsavel por atualizar a senha
@router.post("/reset-password", response_model=MensageResponse)
def update_password(data: ResetPasswordRequest):
    if data.senha != data.confirma_senha:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Senha e Confirma senha não conferem.",
        )

    # Verifica se o token é valido
    user = find_user_reset_token(data.token)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Token de recuperação de senha inválido ou expirado.",
        )
    
    try:
        # Atualiza a senha do usuário
        update_user(user["email"], {"senha": get_password_hash(data.senha), "reset_token": None})
        return MensageResponse(mensagem="Senha atualizada com sucesso.")
    except Exception as error:
        # TODO: Adicionar log do erro para depuração
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Ocorreu um erro ao atualizar a senha.",
        )