from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from . import models
from .database import engine
from .routers import categories, menu_items, ingredients, orders

# Criar as tabelas no banco de dados
models.Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Restaurant Menu API",
    description="API RESTful para gerenciar cardápio de restaurante",
    version="1.0.0"
)

# Configurar CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Em produção, especifique as origens permitidas
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Incluir routers
app.include_router(categories.router)
app.include_router(menu_items.router)
app.include_router(ingredients.router)
app.include_router(orders.router)

@app.get("/")
def read_root():
    return {
        "message": "Bem-vindo à API de Cardápio de Restaurante",
        "docs": "/docs",
        "endpoints": {
            "categories": "/categories",
            "menu_items": "/menu-items",
            "ingredients": "/ingredients",
            "orders": "/orders"
        }
    }