import secrets
from datetime import datetime
from typing import List
from fastapi import APIRouter, HTTPException, status, Depends
from app.config import settings
from app.services.database import (
    find_fornecedor_by_email, 
    insert_fornecedor, 
    update_fornecedor, 
    delete_fornecedor,
    find_fornecedor_reset_token,
    insert_metodo_pagamento,
    list_metodos_pagamento_by_email,
    get_metodo_pagamento,
    update_metodo_pagamento_db,
    delete_metodo_pagamento_db,
    list_vendas_by_fornecedor
)
from app.services.security import get_password_hash, verify_password, create_access_token, get_current_user_email
from app.models.auth import TokenResponse, MensageResponse

from app.models.usuario_fornecedor import (
    UserFornecedorCreateSchema,
    UserFornecedorLoginSchema,
    UserFornecedorUpdateSchema,
    ForgotPasswordRequest,
    ForgotPasswordResponse,
    ResetPasswordRequest,
    MetodoPagamento,
    MetodoPagamentoSchema,
    HistoricoVenda,
)

router = APIRouter(prefix="/fornecedores", tags=["Fornecedores"])

# Rota para registro de fornecedor
@router.post("/register", response_model=MensageResponse)
def register_fornecedor(data: UserFornecedorCreateSchema):
    if find_fornecedor_by_email(data.email):
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Email já cadastrado.")
    
    user_data = data.model_dump()
    user_data['senha'] = get_password_hash(user_data['senha'])
    user_data['email'] = user_data['email'].lower().strip()
    
    insert_fornecedor(user_data)
    return {"mensagem": "Fornecedor cadastrado com sucesso."}

# Rota para login de fornecedor
@router.post("/login", response_model=TokenResponse)
def login_fornecedor(data: UserFornecedorLoginSchema):
    user = find_fornecedor_by_email(data.email)
    
    if not user or not verify_password(data.senha, user['senha']):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Credenciais inválidas.")
    
    token = create_access_token({"sub": user['email'], "role": "fornecedor", "nome": user['nome']})
    return {"access_token": token, "token_type": "bearer"}

# Rota para solicitar recuperação de senha
@router.post("/forgot-password", response_model=ForgotPasswordResponse)
def forgot_password(data: ForgotPasswordRequest):
    user = find_fornecedor_by_email(data.email)
    if not user:
        return ForgotPasswordResponse(mensagem="Se um usuário com este email existir, um email de recuperação será enviado.")

    try:
        token = secrets.token_urlsafe(20)
        update_fornecedor(user["email"], {"reset_token": token})
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

# Rota para resetar a senha usando o token de recuperação
@router.post("/reset-password", response_model=MensageResponse)
def update_password(data: ResetPasswordRequest):
    if data.senha != data.confirma_senha:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Senha e Confirma senha não conferem.",
        )

    user = find_fornecedor_reset_token(data.token)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Token de recuperação de senha inválido ou expirado.",
        )
    try:
        update_fornecedor(user["email"], {"senha": get_password_hash(data.senha), "reset_token": None})
        return MensageResponse(mensagem="Senha atualizada com sucesso.")
    except Exception as error:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Token de recuperação de senha inválido ou expirado.", 
        )

# Rota para atualização de perfil
@router.put("/perfil", response_model=MensageResponse)
def update_perfil(data: UserFornecedorUpdateSchema, email: str = Depends(get_current_user_email)):
    # Verifica se o fornecedor existe
    user = find_fornecedor_by_email(email)
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Fornecedor não encontrado.")
    
    # Atualiza apenas os campos fornecidos
    updates = data.model_dump(exclude_unset=True)
    update_fornecedor(email, updates)
    return {"mensagem": "Perfil atualizado com sucesso."}

# Rota para deletar perfil
@router.delete("/perfil", response_model=MensageResponse)
def delete_perfil(email: str = Depends(get_current_user_email)):
    # Verifica se o fornecedor existe
    user = find_fornecedor_by_email(email)
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Fornecedor não encontrado.")
    
    # Deleta o fornecedor do banco de dados
    delete_fornecedor(email)
    return {"mensagem": "Perfil deletado com sucesso."}

# Rotas para métodos de pagamento do fornecedor
@router.post("/metodos-pagamento", response_model=MetodoPagamentoSchema)
def adicionar_metodo_pagamento(data: MetodoPagamento, current_email: str = Depends(get_current_user_email)):
    # Prepara os dados
    metodo_dict = data.model_dump()
    metodo_dict["fornecedor_email"] = current_email
    metodo_dict["data_criacao"] = datetime.now().isoformat()
    
    # Insere no banco
    doc_id = insert_metodo_pagamento(metodo_dict)
    
    # Retorna com ID
    metodo_dict["id"] = doc_id
    return metodo_dict

# Rota para listar métodos de pagamento do fornecedor
@router.get("/metodos-pagamento", response_model=List[MetodoPagamentoSchema])
def listar_metodos_pagamento(current_email: str = Depends(get_current_user_email)):
    return list_metodos_pagamento_by_email(current_email)

# Rota para atualizar método de pagamento
@router.put("/metodos-pagamento/{id}", response_model=MetodoPagamentoSchema)
def atualizar_metodo_pagamento(id: int, data: MetodoPagamento, current_email: str = Depends(get_current_user_email)):
    metodo_existente = get_metodo_pagamento(id)
    
    if not metodo_existente or metodo_existente.get("fornecedor_email") != current_email:
        raise HTTPException(status_code=404, detail="Método de pagamento não encontrado.")
    
    updates = data.model_dump()
    updates["data_atualizacao"] = datetime.now().isoformat()
    
    update_metodo_pagamento_db(id, updates)
    
    # Mescla os dados existentes com os novos para retorno
    metodo_existente.update(updates)
    return metodo_existente

# Rota para deletar método de pagamento
@router.delete("/metodos-pagamento/{id}", response_model=MensageResponse)
def remover_metodo_pagamento(id: int, current_email: str = Depends(get_current_user_email)):
    metodo_existente = get_metodo_pagamento(id)
    
    if not metodo_existente or metodo_existente.get("fornecedor_email") != current_email:
        raise HTTPException(status_code=404, detail="Método de pagamento não encontrado.")
        
    delete_metodo_pagamento_db(id)
    return {"mensagem": "Método de pagamento removido com sucesso."}

# Rota para listar histórico de vendas do fornecedor
@router.get("/historico-vendas", response_model=List[HistoricoVenda])
def listar_historico_vendas(current_email: str = Depends(get_current_user_email)):
    return list_vendas_by_fornecedor(current_email)