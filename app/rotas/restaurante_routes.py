from fastapi import APIRouter, HTTPException, status
from app.models.usuario_restaurante import UserRestauranteCreateSchema, UserRestauranteLoginSchema
from app.services.database import find_restaurante_by_email, insert_restaurante
from app.services.security import get_password_hash, verify_password, create_access_token
from app.models.auth import TokenResponse, MensageResponse

router = APIRouter(prefix="/restaurantes", tags=["Restaurantes"])

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

@router.post("/login", response_model=TokenResponse)
def login_restaurante(data: UserRestauranteLoginSchema):
    user = find_restaurante_by_email(data.email)
    
    if not user or not verify_password(data.senha, user['senha']):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Credenciais inválidas.")
    
    # Cria token com role específica
    token = create_access_token({"sub": user['email'], "role": "restaurante", "nome": user['nome']})
    return {"access_token": token, "token_type": "bearer"}