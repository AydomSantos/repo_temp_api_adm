"""
Acessa ao Banco de dados TinyDB

- um banco no-sql baseado em arquivos JSON

"""

import os
from tinydb import TinyDB, Query

from app.config import settings 

# Instancia global do banco, apontando para um arquivo JSON
os.makedirs(os.path.dirname(settings.database_path), exist_ok=True)
db = TinyDB(settings.database_path)

# Representando uma "tabela" que armazena usuario
users_table = db.table("users")
restaurantes_table = db.table("restaurantes")
fornecedores_table = db.table("fornecedores")
produtos_table = db.table("produtos")
pedidos_table = db.table("pedidos")
metodos_pagamento_table = db.table("metodos_pagamento")

def find_user_by_email(email: str):
    # Retorna usuario por email ou None, se não existir
    users_query = Query()
    return users_table.get(users_query.email == email.lower().strip())

def find_user_reset_token(token: str):
    # Busca Usuario pelo token de reculperação de senha
    users_query = Query()
    return users_table.get(users_query.reset_token == token)

def insert_user(user_data: dict):
    # Insere um novo usuario no banco
    users_table.insert(user_data)

def update_user(email : str, updates : dict):
    # Atualiza um usuario no banco
    users_query = Query()
    users_table.update(updates, users_query.email == email.lower().strip())

# --- Funções para Restaurantes ---
def find_restaurante_by_email(email: str):
    query = Query()
    return restaurantes_table.get(query.email == email.lower().strip())

def insert_restaurante(data: dict):
    return restaurantes_table.insert(data)

def update_restaurante(email: str, updates: dict):
    query = Query()
    restaurantes_table.update(updates, query.email == email.lower().strip())

def delete_restaurante(email: str):
    query = Query()
    restaurantes_table.remove(query.email == email.lower().strip())

# --- Funções para Fornecedores ---
def find_fornecedor_by_email(email: str):
    query = Query()
    return fornecedores_table.get(query.email == email.lower().strip())

def insert_fornecedor(data: dict):
    return fornecedores_table.insert(data)

def update_fornecedor(email: str, updates: dict):
    query = Query()
    fornecedores_table.update(updates, query.email == email.lower().strip())

def delete_fornecedor(email: str):
    query = Query()
    fornecedores_table.remove(query.email == email.lower().strip())

def find_fornecedor_reset_token(token: str):
    query = Query()
    return fornecedores_table.get(query.reset_token == token)

# --- Funções para Produtos ---
def insert_produto(data: dict):
    return produtos_table.insert(data)

def list_produtos():
    # TinyDB retorna dicts, injetamos o doc_id como 'id' para o frontend
    items = []
    for item in produtos_table.all():
        item['id'] = item.doc_id
        items.append(item)
    return items

def get_produto(id: int):
    item = produtos_table.get(doc_id=id)
    if item:
        item['id'] = item.doc_id
    return item

def update_produto(id: int, data: dict):
    # Atualiza pelo ID do documento
    produtos_table.update(data, doc_ids=[id])

def delete_produto(id: int):
    produtos_table.remove(doc_ids=[id])

# --- Funções para Pedidos (Pagamento) ---
def insert_pedido(data: dict):
    return pedidos_table.insert(data)

def update_pedido_status(session_id: str, status: str):
    query = Query()
    pedidos_table.update({"status": status}, query.session_id == session_id)

def get_pedido_by_session(session_id: str):
    query = Query()
    return pedidos_table.get(query.session_id == session_id)

# --- Funções para Métodos de Pagamento (Fornecedor) ---
def insert_metodo_pagamento(data: dict):
    return metodos_pagamento_table.insert(data)

def list_metodos_pagamento_by_email(email: str):
    query = Query()
    items = metodos_pagamento_table.search(query.fornecedor_email == email.lower().strip())
    for item in items:
        item['id'] = item.doc_id
    return items

def get_metodo_pagamento(id: int):
    item = metodos_pagamento_table.get(doc_id=id)
    if item:
        item['id'] = item.doc_id
    return item

def update_metodo_pagamento_db(id: int, data: dict):
    metodos_pagamento_table.update(data, doc_ids=[id])

def delete_metodo_pagamento_db(id: int):
    metodos_pagamento_table.remove(doc_ids=[id])

# --- Funções para Histórico de Vendas ---
def list_vendas_by_fornecedor(email: str):
    # TODO: Implementar filtro real quando os pedidos tiverem vínculo direto com fornecedor
    # Por enquanto retorna lista vazia ou lógica simulada
    return []
