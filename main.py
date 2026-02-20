from fastapi import FastAPI
import uvicorn
from app.rotas.auth_routes import router as auth_router
from app.rotas.restaurante_routes import router as restaurante_router
from app.rotas.fornecedor_routes import router as fornecedor_router
from app.rotas.produto_routes import router as produto_router
from app.rotas.payment_routes import router as payment_router
#from app.rotas.produto_routes import router as produto_router

app = FastAPI(
    title="Sistema de Autenticação",
    description="API para gerenciamento de usuários e autenticação",
    version="1.0.0"
)

# Inclui as rotas da API
#app.include_router(auth_router)
app.include_router(restaurante_router)
app.include_router(fornecedor_router)
app.include_router(produto_router)
app.include_router(payment_router)

if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
