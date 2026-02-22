"""
Arquivo Principal da Aplicação FastAPI

Este arquivo configura e inicia o servidor da API com todas as rotas.
Utiliza FastAPI para criar uma aplicação web de alta performance.

Autor: Seu Nome
Versão: 1.0.0
"""

# Importações
from fastapi import FastAPI  # Framework web
import uvicorn  # Servidor ASGI para rodar a aplicação

# Importação dos roteadores (rotas) de cada módulo
from app.rotas.auth_routes import router as auth_router  # Rotas de autenticação geral
from app.rotas.restaurante_routes import router as restaurante_router  # Rotas de restaurantes
from app.rotas.fornecedor_routes import router as fornecedor_router  # Rotas de fornecedores
from app.rotas.produto_routes import router as produto_router  # Rotas de produtos
from app.rotas.payment_routes import router as payment_routes  # Rotas de pagamento

# Criação da instância da aplicação FastAPI
# Configurações principais:
# - title: Nome da API (aparece na documentação)
# - description: Descrição do que a API faz
# - version: Versão atual da API
app = FastAPI(
    title="Sistema de Autenticação",  # Título da API
    description="API para gerenciamento de usuários e autenticação",  # Descrição
    version="1.0.0"  # Versão da API
)

# Incluir os roteadores na aplicação principal
# Cada roteador contém um conjunto de endpoints relacionados
# O prefixo é definido em cada router (ex: /restaurantes, /fornecedores)

# app.include_router(auth_router)  # ❌ Descomentado para testes
app.include_router(restaurante_router)  # ✅ Rotas de restaurantes
app.include_router(fornecedor_router)  # ✅ Rotas de fornecedores
app.include_router(produto_router)  # ✅ Rotas de produtos
app.include_router(payment_routes)  # ✅ Rotas de pagamento

# Ponto de entrada da aplicação
if __name__ == "__main__":
    # Inicia o servidor Uvicorn com a aplicação FastAPI
    # Parâmetros:
    # - host: Endereço IP onde o servidor vai rodar (127.0.0.1 = localhost)
    # - port: Porta para acessar a aplicação (padrão HTTP = 8000)
    # - reload: Recarrega o servidor ao detectar mudanças no código (desenvolvimento)
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
