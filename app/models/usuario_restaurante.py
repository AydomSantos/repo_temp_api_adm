from pydantic import BaseModel, EmailStr, Field
from typing import Optional
from datetime import datetime

# Schemas para o modelo de usuário do restaurante
class UserRestauranteCreateSchema(BaseModel):
    nome: str
    email: EmailStr
    senha: str
    numero: int
    cnpj: str

# Schema para atualizar os dados do perfil (tudo opcional)
class UserRestauranteSchema(UserRestauranteCreateSchema):
    id: int

    class Config:
        from_attributes = True

# Schema para atualizar os dados do perfil (tudo opcional)
class UserRestauranteLoginSchema(BaseModel):
    email: EmailStr
    senha: str

# Schema para atualizar os dados do perfil (tudo opcional)
class userRestauranteUpdateSchema(BaseModel):
    nome: Optional[str] = None
    numero: Optional[int] = None
    cnpj: Optional[str] = None
    # Novos campos de perfil
    foto_perfil: Optional[str] = None
    endereco: Optional[str] = None
    cidade: Optional[str] = None
    estado: Optional[str] = None

# Schemas para recuperação de senha
class ForgotPasswordRequest(BaseModel):
    email: EmailStr

# Schema para resposta da solicitação de recuperação de senha
class ForgotPasswordResponse(BaseModel):
    mensagem: str
    token_debug: Optional[str] = None

# Schema para resetar a senha
class ResetPasswordRequest(BaseModel):
    token: str
    senha: str
    confirma_senha: str

# Schemas para o modelo de usuário do fornecedor
class MetodoPagamento(BaseModel):
    metodo: str
    detalhes: str

# Schema para atualizar os dados do perfil (tudo opcional)
class MetodoPagamentoSchema(MetodoPagamento):
    id: int
    data_criacao: datetime = Field(default_factory=datetime.now)
    data_atualizacao: Optional[datetime] = None

# Schemas para o histórico de compras do restaurante
class HistoricoCompra(BaseModel):
    id: int
    id_usuario: int
    id_produto: int
    quantidade: int
    preco_total: float
    data_compra: datetime = Field(default_factory=datetime.now)

# Schema para atualizar os dados do perfil (tudo opcional)
class HistoricoCompraSchema(HistoricoCompra):
    class Config:
        from_attributes = True

class TokenResponse(BaseModel):
    access_token: str
    token_type: str

class MensageResponse(BaseModel):
    mensagem: str