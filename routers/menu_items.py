from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from .. import models, schemas
from ..database import get_db

router = APIRouter(
    prefix="/menu-items",
    tags=["menu items"],
    responses={404: {"description": "Not found"}},
)

@router.post("/", response_model=schemas.MenuItem, status_code=status.HTTP_201_CREATED)
def create_menu_item(menu_item: schemas.MenuItemCreate, db: Session = Depends(get_db)):
    # Verificar se a categoria existe
    db_category = db.query(models.Category).filter(models.Category.id == menu_item.category_id).first()
    if not db_category:
        raise HTTPException(status_code=400, detail="Category not found")
    
    # Criar o item do menu sem os ingredientes
    db_menu_item = models.MenuItem(
        name=menu_item.name,
        description=menu_item.description,
        price=menu_item.price,
        image_url=menu_item.image_url,
        is_available=menu_item.is_available,
        category_id=menu_item.category_id
    )
    db.add(db_menu_item)
    db.commit()
    db.refresh(db_menu_item)
    
    # Adicionar ingredientes se fornecidos
    if menu_item.ingredient_ids:
        ingredients = db.query(models.Ingredient).filter(models.Ingredient.id.in_(menu_item.ingredient_ids)).all()
        if len(ingredients) != len(menu_item.ingredient_ids):
            db.delete(db_menu_item)
            db.commit()
            raise HTTPException(status_code=400, detail="One or more ingredients not found")
        
        db_menu_item.ingredients = ingredients
        db.commit()
        db.refresh(db_menu_item)
    
    return db_menu_item

@router.get("/", response_model=List[schemas.MenuItem])
def read_menu_items(
    skip: int = 0, 
    limit: int = 100, 
    category_id: int = None, 
    available_only: bool = False,
    db: Session = Depends(get_db)
):
    query = db.query(models.MenuItem)
    
    if category_id:
        query = query.filter(models.MenuItem.category_id == category_id)
    
    if available_only:
        query = query.filter(models.MenuItem.is_available == True)
    
    menu_items = query.offset(skip).limit(limit).all()
    return menu_items

@router.get("/{menu_item_id}", response_model=schemas.MenuItem)
def read_menu_item(menu_item_id: int, db: Session = Depends(get_db)):
    db_menu_item = db.query(models.MenuItem).filter(models.MenuItem.id == menu_item_id).first()
    if db_menu_item is None:
        raise HTTPException(status_code=404, detail="Menu item not found")
    return db_menu_item

@router.put("/{menu_item_id}", response_model=schemas.MenuItem)
def update_menu_item(menu_item_id: int, menu_item: schemas.MenuItemUpdate, db: Session = Depends(get_db)):
    db_menu_item = db.query(models.MenuItem).filter(models.MenuItem.id == menu_item_id).first()
    if db_menu_item is None:
        raise HTTPException(status_code=404, detail="Menu item not found")
    
    # Atualizar campos básicos
    update_data = menu_item.dict(exclude_unset=True)
    
    # Remover ingredient_ids do dicionário de atualização
    ingredient_ids = update_data.pop("ingredient_ids", None)
    
    # Verificar se a categoria existe se estiver sendo atualizada
    if "category_id" in update_data and update_data["category_id"] is not None:
        db_category = db.query(models.Category).filter(models.Category.id == update_data["category_id"]).first()
        if not db_category:
            raise HTTPException(status_code=400, detail="Category not found")
    
    # Atualizar os campos básicos
    for key, value in update_data.items():
        setattr(db_menu_item, key, value)
    
    # Atualizar ingredientes se fornecidos
    if ingredient_ids is not None:
        ingredients = db.query(models.Ingredient).filter(models.Ingredient.id.in_(ingredient_ids)).all()
        if len(ingredients) != len(ingredient_ids):
            raise HTTPException(status_code=400, detail="One or more ingredients not found")
        
        db_menu_item.ingredients = ingredients
    
    db.commit()
    db.refresh(db_menu_item)
    return db_menu_item

@router.delete("/{menu_item_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_menu_item(menu_item_id: int, db: Session = Depends(get_db)):
    db_menu_item = db.query(models.MenuItem).filter(models.MenuItem.id == menu_item_id).first()
    if db_menu_item is None:
        raise HTTPException(status_code=404, detail="Menu item not found")
    
    db.delete(db_menu_item)
    db.commit()
    return None