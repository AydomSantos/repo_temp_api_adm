from pydantic import BaseModel, EmailStr
from typing import Optional

class UserRestauranteCreateSchema(BaseModel):
    nome: str
    email: EmailStr
    senha: str
    numero: int
    cnpj: str

class UserRestauranteSchema(UserRestauranteCreateSchema):
    id: int

    class Config:
        from_attributes = True

class UserRestauranteLoginSchema(BaseModel):
    email: EmailStr
    senha: str