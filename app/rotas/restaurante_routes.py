"""
Rotas de restaurante.

Inclui cadastro, login, recuperacao de senha e operacoes de perfil.
"""

import secrets

from fastapi import APIRouter, Depends, HTTPException, status

from app.config import settings
from app.models.usuario_restaurante import (
    ForgotPasswordRequest,
    ForgotPasswordResponse,
    HistoricoCompraSchema,
    MetodoPagamento,
    MetodoPagamentoSchema,
    ResetPasswordRequest,
    UserRestauranteCreateSchema,
    UserRestauranteLoginSchema,
    userRestauranteUpdateSchema,
    TokenResponse,
    MensageResponse,
)
from app.services.database import (
    delete_restaurante,
    find_restaurante_by_email,
    find_restaurante_reset_token,
    insert_restaurante,
    update_restaurante,
)
from app.services.security import create_access_token, get_password_hash, require_role, verify_password

router = APIRouter(prefix="/restaurantes", tags=["Restaurantes"])


@router.post("/register", response_model=MensageResponse)
def register_restaurante(data: UserRestauranteCreateSchema):
    if find_restaurante_by_email(data.email):
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Email ja cadastrado.")

    # Armazena senha com hash e dados normalizados.
    user_data = data.model_dump()
    user_data["senha"] = get_password_hash(user_data["senha"])
    user_data["email"] = user_data["email"].lower().strip()
    user_data["ativo"] = True
    user_data["reset_token"] = None

    insert_restaurante(user_data)
    return {"mensagem": "Restaurante cadastrado com sucesso."}


@router.post("/login", response_model=TokenResponse)
def login_restaurante(data: UserRestauranteLoginSchema):
    user = find_restaurante_by_email(data.email)

    if not user or not verify_password(data.senha, user["senha"]):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Credenciais invalidas.")

    if not user.get("ativo", True):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Usuario inativo.")

    token = create_access_token({"sub": user["email"], "role": "restaurante", "nome": user["nome"]})
    return {"access_token": token, "token_type": "bearer"}


@router.post("/forgot-password", response_model=ForgotPasswordResponse)
def forgot_password(data: ForgotPasswordRequest):
    user = find_restaurante_by_email(data.email)
    safe_msg = "Se um usuario com este email existir, um email de recuperacao sera enviado."
    if not user or not user.get("ativo", True):
        return ForgotPasswordResponse(mensagem=safe_msg)

    token = secrets.token_urlsafe(20)
    update_restaurante(user["email"], {"reset_token": token})

    response = {"mensagem": safe_msg}
    if settings.debug_password_reset_token:
        response["token_debug"] = token
    return ForgotPasswordResponse(**response)


@router.post("/reset-password", response_model=MensageResponse)
def update_password(data: ResetPasswordRequest):
    if data.senha != data.confirma_senha:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="As senhas nao coincidem.")

    user = find_restaurante_reset_token(data.token)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Token de recuperacao de senha invalido ou expirado.",
        )

    update_restaurante(user["email"], {"senha": get_password_hash(data.senha), "reset_token": None})
    return {"mensagem": "Senha atualizada com sucesso."}


@router.put("/perfil", response_model=MensageResponse)
def update_perfil(data: userRestauranteUpdateSchema, email: str = Depends(require_role("restaurante"))):
    user = find_restaurante_by_email(email)
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Restaurante nao encontrado.")

    updates = data.model_dump(exclude_unset=True)
    update_restaurante(email, updates)
    return {"mensagem": "Perfil atualizado com sucesso."}


@router.delete("/perfil", response_model=MensageResponse)
def delete_perfil(email: str = Depends(require_role("restaurante"))):
    user = find_restaurante_by_email(email)
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Restaurante nao encontrado.")

    delete_restaurante(email)
    return {"mensagem": "Perfil deletado com sucesso."}


@router.post("/metodos-pagamento", response_model=MetodoPagamentoSchema)
def adicionar_metodo_pagamento(data: MetodoPagamento, email: str = Depends(require_role("restaurante"))):
    user = find_restaurante_by_email(email)
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Restaurante nao encontrado.")

    # Placeholder enquanto nao houver tabela especifica de metodos do restaurante.
    return MetodoPagamentoSchema(id=1, metodo=data.metodo, detalhes=data.detalhes)


@router.get("/historico-compras", response_model=list[HistoricoCompraSchema])
def obter_historico_compras(email: str = Depends(require_role("restaurante"))):
    user = find_restaurante_by_email(email)
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Restaurante nao encontrado.")

    # Placeholder de historico ate existir relacao real com pedidos.
    return [HistoricoCompraSchema(id=1, id_usuario=1, id_produto=1, quantidade=2, preco_total=100.0)]
