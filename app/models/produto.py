
from pydantic import BaseModel, Field
from typing import Optional
from datetime import date

class ProdutoCreateSchema(BaseModel):
    # Informações Básicas
    nome_produto: str = Field(..., example="Tomate Italiano")
    categoria: Optional[str] = Field(None, example="Legumes")
    fornecedor_id: int
    
    # Tipo e Preço (Refletindo os Checkboxes e inputs da imagem)
    vende_varejo: bool = False
    vende_atacado: bool = False
    preco_varejo: Optional[float] = None
    preco_atacado: Optional[float] = None
    
    # Estoque
    estoque_inicial: int = Field(default=0, ge=0)
    
    # Logística de Entrega
    tipo_entrega: Optional[str] = None # Ex: "Própria" ou "Terceirizada"
    custo_adicional: float = 0.0
    prazo_medio: Optional[str] = Field(None, example="3-5")
    
    # Promoção
    promocao_data_inicio: Optional[date] = None
    promocao_data_fim: Optional[date] = None
    desconto_percentual: Optional[float] = None

    class Config:
        from_attributes = True # Permite converter modelos do banco (ORM) para o Schema
    
class ProdutoSchema(ProdutoCreateSchema):
    id: int

    class Config:
        from_attributes = True
        