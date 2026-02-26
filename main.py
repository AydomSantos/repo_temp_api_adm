"""
Ponto de entrada da API FastAPI.

Este arquivo cria a aplicacao e registra todos os roteadores.
"""

from fastapi import FastAPI
import uvicorn

# Importa cada grupo de rotas da aplicacao.

from app.rotas.fornecedor_routes import router as fornecedor_router
from app.rotas.payment_routes import router as payment_routes
from app.rotas.produto_routes import router as produto_router
from app.rotas.restaurante_routes import router as restaurante_router

# Configuracao basica exibida na documentacao Swagger.
app = FastAPI(
    title="Sistema de Autenticacao",
    description="API para gerenciamento de usuarios e autenticacao",
    version="1.0.0",
)

# Registra os endpoints na aplicacao principal.

app.include_router(restaurante_router)
app.include_router(fornecedor_router)
app.include_router(produto_router)
app.include_router(payment_routes)

# Executa servidor local quando este arquivo for chamado diretamente.
if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
