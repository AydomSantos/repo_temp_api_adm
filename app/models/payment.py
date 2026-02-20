from pydantic import BaseModel
from typing import List, Optional

class ItemCarrinho(BaseModel):
    nome: str
    preco_unitario: float # Em reais (ex: 10.50)
    quantidade: int

class CheckoutRequest(BaseModel):
    itens: List[ItemCarrinho]
    email_cliente: str # Para enviar o recibo

class CheckoutResponse(BaseModel):
    checkout_url: str
    session_id: str