from fastapi import APIRouter, HTTPException, status
from typing import List
from app.models.produto import ProdutoCreateSchema, ProdutoSchema
from app.services.database import insert_produto, list_produtos, get_produto, update_produto, delete_produto

router = APIRouter(prefix="/produtos", tags=["Produtos"])

@router.post("/", response_model=ProdutoSchema)
def create_produto(data: ProdutoCreateSchema):
    # Converte para dict e serializa datas para JSON (mode='json')
    prod_data = data.model_dump(mode='json')
    
    # Insere e recupera o ID gerado pelo TinyDB
    doc_id = insert_produto(prod_data)
    
    # Retorna o objeto com o ID injetado
    prod_data['id'] = doc_id
    return prod_data

@router.get("/", response_model=List[ProdutoSchema])
def read_produtos():
    return list_produtos()

@router.get("/{id}", response_model=ProdutoSchema)
def read_produto(id: int):
    prod = get_produto(id)
    if not prod:
        raise HTTPException(status_code=404, detail="Produto não encontrado")
    return prod

@router.put("/{id}", response_model=ProdutoSchema)
def update_produto_route(id: int, data: ProdutoCreateSchema):
    if not get_produto(id):
        raise HTTPException(status_code=404, detail="Produto não encontrado")
    
    prod_data = data.model_dump(mode='json')
    update_produto(id, prod_data)
    prod_data['id'] = id
    return prod_data

@router.delete("/{id}", status_code=204)
def delete_produto_route(id: int):
    if not get_produto(id):
        raise HTTPException(status_code=404, detail="Produto não encontrado")
    delete_produto(id)