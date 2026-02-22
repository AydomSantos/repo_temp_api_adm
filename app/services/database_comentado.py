"""
Serviço de Banco de Dados com TinyDB

Arquivo responsável por todas as operações de banco de dados.
Utiliza TinyDB, um banco NoSQL baseado em arquivos JSON (sem servidor externo).

Tabelas criadas:
- users: Usuários gerais do sistema
- restaurantes: Restaurantes cadastrados
- fornecedores: Fornecedores cadastrados
- produtos: Catálogo de produtos
- pedidos: Histórico de pedidos e pagamentos
- metodos_pagamento: Métodos de pagamento dos fornecedores

Autor: Seu Nome
"""

import os  # Manipulação do sistema de arquivos
from tinydb import TinyDB, Query  # Banco de dados NoSQL e queries

from app.config import settings  # Configurações da aplicação

# ============ CONFIGURAÇÃO DO BANCO ============
# Cria o diretório 'data' se não existir (exist_ok=True evita erro se já existe)
os.makedirs(os.path.dirname(settings.database_path), exist_ok=True)

# Instancia global (singleton) do banco de dados TinyDB
# Aponta para database.json em {BACK_ROOT}/data/
db = TinyDB(settings.database_path)

# ============ DEFINIÇÃO DAS TABELAS ============
# TinyDB permite múltiplas "tabelas" dentro do mesmo arquivo JSON
# Cada tabela é uma coleção independente de documentos
users_table = db.table("users")  # Tabela de usuários gerais
restaurantes_table = db.table("restaurantes")  # Tabela de restaurantes
fornecedores_table = db.table("fornecedores")  # Tabela de fornecedores
produtos_table = db.table("produtos")  # Tabela de produtos
pedidos_table = db.table("pedidos")  # Tabela de pedidos/pagamentos
metodos_pagamento_table = db.table("metodos_pagamento")  # Tabela de métodos de pagamento

# ============ FUNÇÕES PARA USUÁRIOS GERAIS ============

def find_user_by_email(email: str):
    """
    Busca um usuário pelo email.
    
    Parâmetros:
        email (str): Email do usuário a buscar
    
    Retorna:
        dict: Dados do usuário se encontrado, None caso contrário
    """
    # Query() cria um objeto para fazer buscas na tabela
    users_query = Query()
    # .get() retorna o primeiro documento que corresponde à condição
    # .lower().strip() normaliza o email para padronização
    return users_table.get(users_query.email == email.lower().strip())

def find_user_reset_token(token: str):
    """
    Busca um usuário pelo token de recuperação de senha.
    
    Parâmetros:
        token (str): Token de recuperação de senha
    
    Retorna:
        dict: Usuário encontrado, None caso contrário
    """
    users_query = Query()
    return users_table.get(users_query.reset_token == token)

def insert_user(user_data: dict):
    """
    Insere um novo usuário no banco.
    
    Parâmetros:
        user_data (dict): Dicionário com os dados do usuário
                          Deve conter: nome, email, senha (hash), numero, cnpj
    
    Retorna:
        int: ID do documento inserido
    """
    return users_table.insert(user_data)

def update_user(email: str, updates: dict):
    """
    Atualiza os dados de um usuário existente.
    
    Parâmetros:
        email (str): Email do usuário a atualizar
        updates (dict): Dicionário com os campos a atualizar
    """
    users_query = Query()
    users_table.update(updates, users_query.email == email.lower().strip())

# ============ FUNÇÕES PARA RESTAURANTES ============

def find_restaurante_by_email(email: str):
    """
    Busca um restaurante pelo email.
    
    Parâmetros:
        email (str): Email do restaurante
    
    Retorna:
        dict: Dados do restaurante, None se não encontrado
    """
    query = Query()
    return restaurantes_table.get(query.email == email.lower().strip())

def insert_restaurante(data: dict):
    """
    Insere um novo restaurante.
    
    Parâmetros:
        data (dict): Dados do restaurante
    
    Retorna:
        int: ID do documento inserido
    """
    return restaurantes_table.insert(data)

def update_restaurante(email: str, updates: dict):
    """
    Atualiza um restaurante existente.
    
    Parâmetros:
        email (str): Email do restaurante
        updates (dict): Campos a atualizar
    """
    query = Query()
    restaurantes_table.update(updates, query.email == email.lower().strip())

def delete_restaurante(email: str):
    """
    Deleta um restaurante do banco.
    
    Parâmetros:
        email (str): Email do restaurante a deletar
    """
    query = Query()
    restaurantes_table.remove(query.email == email.lower().strip())

# ============ FUNÇÕES PARA FORNECEDORES ============

def find_fornecedor_by_email(email: str):
    """
    Busca um fornecedor pelo email.
    
    Parâmetros:
        email (str): Email do fornecedor
    
    Retorna:
        dict: Dados do fornecedor, None se não encontrado
    """
    query = Query()
    return fornecedores_table.get(query.email == email.lower().strip())

def insert_fornecedor(data: dict):
    """
    Insere um novo fornecedor.
    
    Parâmetros:
        data (dict): Dados do fornecedor
    
    Retorna:
        int: ID do documento inserido
    """
    return fornecedores_table.insert(data)

def update_fornecedor(email: str, updates: dict):
    """
    Atualiza um fornecedor existente.
    
    Parâmetros:
        email (str): Email do fornecedor
        updates (dict): Campos a atualizar
    """
    query = Query()
    fornecedores_table.update(updates, query.email == email.lower().strip())

def delete_fornecedor(email: str):
    """
    Deleta um fornecedor do banco.
    
    Parâmetros:
        email (str): Email do fornecedor a deletar
    """
    query = Query()
    fornecedores_table.remove(query.email == email.lower().strip())

def find_fornecedor_reset_token(token: str):
    """
    Busca um fornecedor pelo token de recuperação de senha.
    
    Parâmetros:
        token (str): Token de recuperação
    
    Retorna:
        dict: Fornecedor encontrado, None caso contrário
    """
    query = Query()
    return fornecedores_table.get(query.reset_token == token)

# ============ FUNÇÕES PARA PRODUTOS ============

def insert_produto(data: dict):
    """
    Insere um novo produto.
    
    Parâmetros:
        data (dict): Dados do produto com nome_produto, categoria, preço, estoque, etc
    
    Retorna:
        int: ID (doc_id) do produto inserido
    """
    return produtos_table.insert(data)

def list_produtos():
    """
    Lista todos os produtos do banco.
    
    Retorna:
        list: Lista de produtos com 'id' adicionado
    
    Nota: Injeta o doc_id como 'id' para consistência com frontend
    """
    items = []
    # .all() retorna todos os documentos da tabela
    for item in produtos_table.all():
        # TinyDB usa doc_id internamente, convertemos para 'id' para o frontend
        item['id'] = item.doc_id
        items.append(item)
    return items

def get_produto(id: int):
    """
    Busca um produto por ID.
    
    Parâmetros:
        id (int): ID/doc_id do produto
    
    Retorna:
        dict: Dados do produto com 'id' adicionado, None se não encontrado
    """
    # .get(doc_id=id) busca por ID do documento
    item = produtos_table.get(doc_id=id)
    if item:
        item['id'] = item.doc_id  # Adiciona o id para retorno
    return item

def update_produto(id: int, data: dict):
    """
    Atualiza um produto existente.
    
    Parâmetros:
        id (int): ID do produto
        data (dict): Dados a atualizar
    """
    # Atualiza pelo ID do documento
    produtos_table.update(data, doc_ids=[id])

def delete_produto(id: int):
    """
    Deleta um produto.
    
    Parâmetros:
        id (int): ID do produto a deletar
    """
    # Remove pelo ID do documento
    produtos_table.remove(doc_ids=[id])

# ============ FUNÇÕES PARA PEDIDOS (PAGAMENTO) ============

def insert_pedido(data: dict):
    """
    Insere um novo pedido/pagamento.
    
    Parâmetros:
        data (dict): Dados do pedido (itens, total, status, session_id, etc)
    
    Retorna:
        int: ID do pedido inserido
    """
    return pedidos_table.insert(data)

def update_pedido_status(session_id: str, status: str):
    """
    Atualiza o status de um pedido pela session_id do Stripe.
    
    Parâmetros:
        session_id (str): ID da sessão de checkout do Stripe
        status (str): Novo status (ex: 'paid', 'pending', 'canceled')
    """
    query = Query()
    pedidos_table.update({"status": status}, query.session_id == session_id)

def get_pedido_by_session(session_id: str):
    """
    Busca um pedido pela session_id do Stripe.
    
    Parâmetros:
        session_id (str): ID da sessão de checkout do Stripe
    
    Retorna:
        dict: Dados do pedido, None se não encontrado
    """
    query = Query()
    return pedidos_table.get(query.session_id == session_id)

# ============ FUNÇÕES PARA MÉTODOS DE PAGAMENTO ============

def insert_metodo_pagamento(data: dict):
    """
    Insere um novo método de pagamento para um fornecedor.
    
    Parâmetros:
        data (dict): Deve conter 'fornecedor_email', 'metodo', 'detalhes', etc
    
    Retorna:
        int: ID do método de pagamento inserido
    """
    return metodos_pagamento_table.insert(data)

def list_metodos_pagamento_by_email(email: str):
    """
    Lista todos os métodos de pagamento de um fornecedor.
    
    Parâmetros:
        email (str): Email do fornecedor
    
    Retorna:
        list: Lista de métodos de pagamento do fornecedor com 'id' adicionado
    """
    query = Query()
    # .search() retorna todos os documentos que correspondem à condição
    items = metodos_pagamento_table.search(query.fornecedor_email == email.lower().strip())
    # Adiciona 'id' a cada método (cópia do doc_id)
    for item in items:
        item['id'] = item.doc_id
    return items

def get_metodo_pagamento(id: int):
    """
    Busca um método de pagamento por ID.
    
    Parâmetros:
        id (int): ID do método de pagamento
    
    Retorna:
        dict: Dados do método com 'id' adicionado, None se não encontrado
    """
    item = metodos_pagamento_table.get(doc_id=id)
    if item:
        item['id'] = item.doc_id
    return item

def update_metodo_pagamento_db(id: int, data: dict):
    """
    Atualiza um método de pagamento existente.
    
    Parâmetros:
        id (int): ID do método
        data (dict): Dados a atualizar
    """
    metodos_pagamento_table.update(data, doc_ids=[id])

def delete_metodo_pagamento_db(id: int):
    """
    Deleta um método de pagamento.
    
    Parâmetros:
        id (int): ID do método a deletar
    """
    metodos_pagamento_table.remove(doc_ids=[id])

# ============ FUNÇÕES PARA HISTÓRICO DE VENDAS ============

def list_vendas_by_fornecedor(email: str):
    """
    Lista o histórico de vendas de um fornecedor.
    
    Parâmetros:
        email (str): Email do fornecedor
    
    Retorna:
        list: Histórico de vendas (atualmente lista vazia, implementar)
    
    TODO: Implementar filtro real quando os pedidos tiverem vínculo direto com fornecedor
    """
    # Placeholder - retorna lista vazia por enquanto
    # Será implementado quando a estrutura de vendas for definida
    return []
