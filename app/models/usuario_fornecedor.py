from pydantic import BaseModel, EmailStr, Field
from datetime import datetime
from typing import Optional

class UserFornecedorCreateSchema(BaseModel):
    nome: str
    email: EmailStr
    senha: str
    numero: int
    cnpj: str

# Schema para atualizar os dados do perfil (tudo opcional)
class UserFornecedorUpdateSchema(BaseModel):
    nome: Optional[str] = None
    numero: Optional[int] = None
    cnpj: Optional[str] = None
    # Novos campos de perfil
    foto_perfil: Optional[str] = None
    endereco: Optional[str] = None
    cidade: Optional[str] = None
    estado: Optional[str] = None

# Schema para atualizar os dados do perfil (tudo opcional)
class UserFornecedorSchema(UserFornecedorCreateSchema):
    id: int
    foto_perfil: Optional[str] = None
    endereco: Optional[str] = None
    cidade: Optional[str] = None
    estado: Optional[str] = None

    class Config:
        from_attributes = True
# Schema para login do fornecedor
class UserFornecedorLoginSchema(BaseModel):
    email: EmailStr
    senha: str
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
# Schemas para o histórico de vendas do fornecedor
class HistoricoVenda(BaseModel):
    id: int
    produto_id: int
    quantidade: int
    valor_total: float
    data_venda: datetime

class TokenResponse(BaseModel):
    access_token: str
    token_type: str

class MensageResponse(BaseModel):
    mensagem: str