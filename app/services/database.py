"""
Camada de acesso ao TinyDB.

Centraliza operacoes de leitura/escrita para usuarios, restaurantes,
fornecedores, produtos, pedidos e metodos de pagamento.
"""

import os

from tinydb import Query, TinyDB

from app.config import settings

# Garante que a pasta do arquivo JSON exista antes de abrir o banco.
os.makedirs(os.path.dirname(settings.database_path), exist_ok=True)
db = TinyDB(settings.database_path)

# "Tabelas" logicas dentro do arquivo JSON do TinyDB.
restaurantes_table = db.table("restaurantes")
fornecedores_table = db.table("fornecedores")
produtos_table = db.table("produtos")
pedidos_table = db.table("pedidos")
metodos_pagamento_table = db.table("metodos_pagamento")


# ---------- Usuarios gerais ----------
def find_user_by_email(email: str):
    query = Query()
    return users_table.get(query.email == email.lower().strip())


def find_user_reset_token(token: str):
    query = Query()
    return users_table.get(query.reset_token == token)


def insert_user(user_data: dict):
    return users_table.insert(user_data)


def update_user(email: str, updates: dict):
    query = Query()
    users_table.update(updates, query.email == email.lower().strip())


# ---------- Restaurantes ----------
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


def find_restaurante_reset_token(token: str):
    query = Query()
    return restaurantes_table.get(query.reset_token == token)


# ---------- Fornecedores ----------
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


# ---------- Produtos ----------
def insert_produto(data: dict):
    return produtos_table.insert(data)


def list_produtos():
    # Injeta doc_id como "id" para retorno consistente na API.
    items = []
    for item in produtos_table.all():
        item["id"] = item.doc_id
        items.append(item)
    return items


def get_produto(id: int):
    item = produtos_table.get(doc_id=id)
    if item:
        item["id"] = item.doc_id
    return item


def update_produto(id: int, data: dict):
    produtos_table.update(data, doc_ids=[id])


def delete_produto(id: int):
    produtos_table.remove(doc_ids=[id])


# ---------- Pedidos ----------
def insert_pedido(data: dict):
    return pedidos_table.insert(data)


def update_pedido_status(session_id: str, status: str):
    query = Query()
    pedidos_table.update({"status": status}, query.session_id == session_id)


def get_pedido_by_session(session_id: str):
    query = Query()
    return pedidos_table.get(query.session_id == session_id)


# ---------- Metodos de pagamento (fornecedor) ----------
def insert_metodo_pagamento(data: dict):
    return metodos_pagamento_table.insert(data)


def list_metodos_pagamento_by_email(email: str):
    query = Query()
    items = metodos_pagamento_table.search(query.fornecedor_email == email.lower().strip())
    for item in items:
        item["id"] = item.doc_id
    return items


def get_metodo_pagamento(id: int):
    item = metodos_pagamento_table.get(doc_id=id)
    if item:
        item["id"] = item.doc_id
    return item


def update_metodo_pagamento_db(id: int, data: dict):
    metodos_pagamento_table.update(data, doc_ids=[id])


def delete_metodo_pagamento_db(id: int):
    metodos_pagamento_table.remove(doc_ids=[id])


# ---------- Historico de vendas ----------
def list_vendas_by_fornecedor(email: str):
    # Ainda depende do vinculo direto de pedidos ao fornecedor.
    return []
