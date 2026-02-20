from fastapi import APIRouter, HTTPException, status
from app.models.usuario_fornecedor import UserFornecedorCreateSchema, UserFornecedorLoginSchema
from app.services.database import find_fornecedor_by_email, insert_fornecedor
from app.services.security import get_password_hash, verify_password, create_access_token
from app.models.auth import TokenResponse, MensageResponse

router = APIRouter(prefix="/fornecedores", tags=["Fornecedores"])

@router.post("/register", response_model=MensageResponse)
def register_fornecedor(data: UserFornecedorCreateSchema):
    if find_fornecedor_by_email(data.email):
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Email já cadastrado.")
    
    user_data = data.model_dump()
    user_data['senha'] = get_password_hash(user_data['senha'])
    user_data['email'] = user_data['email'].lower().strip()
    
    insert_fornecedor(user_data)
    return {"mensagem": "Fornecedor cadastrado com sucesso."}

@router.post("/login", response_model=TokenResponse)
def login_fornecedor(data: UserFornecedorLoginSchema):
    user = find_fornecedor_by_email(data.email)
    
    if not user or not verify_password(data.senha, user['senha']):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Credenciais inválidas.")
    
    token = create_access_token({"sub": user['email'], "role": "fornecedor", "nome": user['nome']})
    return {"access_token": token, "token_type": "bearer"}