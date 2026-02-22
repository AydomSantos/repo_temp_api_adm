from fastapi import APIRouter, HTTPException, status, Depends

from app.services.database import find_restaurante_by_email, insert_restaurante, update_restaurante, delete_restaurante
from app.services.security import get_password_hash, verify_password, create_access_token, get_current_user_email
from app.models.usuario_restaurante import (
    UserRestauranteCreateSchema,
    UserRestauranteLoginSchema,
    userRestauranteUpdateSchema,
    ForgotPasswordRequest,
    ForgotPasswordResponse,
    ResetPasswordRequest,
    MetodoPagamento,
    MetodoPagamentoSchema,
    HistoricoCompra,
    HistoricoCompraSchema,
)

router = APIRouter(prefix="/restaurantes", tags=["Restaurantes"])

# Rota para registro de restaurante
@router.post("/register", response_model=MensageResponse)
def register_restaurante(data: UserRestauranteCreateSchema):
    # Verifica se email já existe
    if find_restaurante_by_email(data.email):
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Email já cadastrado.")
    
    # Prepara dados para salvar
    user_data = data.model_dump()
    user_data['senha'] = get_password_hash(user_data['senha'])
    user_data['email'] = user_data['email'].lower().strip()
    
    insert_restaurante(user_data)
    return {"mensagem": "Restaurante cadastrado com sucesso."}

# Rota para login de restaurante
@router.post("/login", response_model=TokenResponse)
def login_restaurante(data: UserRestauranteLoginSchema):
    user = find_restaurante_by_email(data.email)
    
    if not user or not verify_password(data.senha, user['senha']):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Credenciais inválidas.")
    
    # Cria token com role específica
    token = create_access_token({"sub": user['email'], "role": "restaurante", "nome": user['nome']})
    return {"access_token": token, "token_type": "bearer"}

# Rota para solicitar recuperação de senha
@router.post("/forgot-password", response_model=ForgotPasswordResponse)
def forgot_password(data: ForgotPasswordRequest):
    user = find_restaurante_by_email(data.email)
    if not user:
        return ForgotPasswordResponse(mensagem="Se um usuário com este email existir, um email de recuperação será enviado.")
    # Aqui você geraria um token de recuperação e enviaria por email
    token_debug = create_access_token({"sub": user['email'], "role": "restaurante", "nome": user['nome']})
    return ForgotPasswordResponse(mensagem="Se um usuário com este email existir, um email de recuperação será enviado.", token_debug=token_debug)

# Rota para resetar a senha usando o token de recuperação
@router.post("/reset-password", response_model=MensageResponse)
def update_password(data: ResetPasswordRequest):
    # Aqui você validaria o token e atualizaria a senha do usuário
    if data.senha != data.confirma_senha:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="As senhas não coincidem.")
    # Lógica para atualizar a senha do usuário no banco de dados
    return {"mensagem": "Senha atualizada com sucesso."}

# Rota para atualização de perfil
@router.put("/perfil", response_model=MensageResponse)
def update_perfil(data: userRestauranteUpdateSchema, email: str = Depends(get_current_user_email)):
    # Verifica se o restaurante existe
    user = find_restaurante_by_email(email)
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Restaurante não encontrado.")
    
    # Atualiza apenas os campos fornecidos
    updates = data.model_dump(exclude_unset=True)
    update_restaurante(email, updates)
    return {"mensagem": "Perfil atualizado com sucesso."}

# Rota para deletar perfil
@router.delete("/perfil", response_model=MensageResponse)
def delete_perfil(email: str = Depends(get_current_user_email)):
    # Verifica se o restaurante existe
    user = find_restaurante_by_email(email)
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Restaurante não encontrado.")
    
    # Deleta o restaurante do banco de dados
    delete_restaurante(email)
    return {"mensagem": "Perfil deletado com sucesso."}

# Rotas para métodos de pagamento do restaurante
@router.post("/metodos-pagamento", response_model=MetodoPagamentoSchema)
def adicionar_metodo_pagamento(data: MetodoPagamento, email: str = Depends(get_current_user_email)):
    # Verifica se o restaurante existe
    user = find_restaurante_by_email(email)
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Restaurante não encontrado.")
    
    # Lógica para adicionar método de pagamento ao restaurante
    return MetodoPagamentoSchema(id=1, metodo=data.metodo, detalhes=data.detalhes)

# Rota para listar métodos de pagamento do restaurante
@router.get("/historico-compras", response_model=list[HistoricoCompraSchema])
def obter_historico_compras(email: str = Depends(get_current_user_email)):
    # Verifica se o restaurante existe
    user = find_restaurante_by_email(email)
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Restaurante não encontrado.")
    
    # Lógica para obter histórico de compras do restaurante
    return [
        HistoricoCompraSchema(id=1, id_usuario=1, itens=["Item 1", "Item 2"], preco_total=100.0)
    ]

