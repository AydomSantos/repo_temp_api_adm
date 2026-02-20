from pydantic import BaseModel, EmailStr
from typing import Optional

class UserFornecedorCreateSchema(BaseModel):
    nome: str
    email: EmailStr
    senha: str
    numero: int
    cnpj: str

class UserFornecedorSchema(UserFornecedorCreateSchema):
    id: int

    class Config:
        from_attributes = True

class UserFornecedorLoginSchema(BaseModel):
    email: EmailStr
    senha: str