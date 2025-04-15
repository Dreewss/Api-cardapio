from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from datetime import datetime

from .. import models, schemas
from ..database import get_db

router = APIRouter(
    prefix="/orders",
    tags=["orders"],
    responses={404: {"description": "Not found"}},
)

@router.post("/", response_model=schemas.Order, status_code=status.HTTP_201_CREATED)
def create_order(order: schemas.OrderCreate, db: Session = Depends(get_db)):
    # Criar o pedido
    db_order = models.Order(
        table_number=order.table_number,
        customer_name=order.customer_name,
        status=order.status,
        created_at=datetime.now().isoformat()
    )
    db.add(db_order)
    db.commit()
    db.refresh(db_order)
    
    # Adicionar itens ao pedido
    for item in order.items:
        # Verificar se o item do menu existe
        menu_item = db.query(models.MenuItem).filter(models.MenuItem.id == item.menu_item_id).first()
        if not menu_item:
            db.delete(db_order)
            db.commit()
            raise HTTPException(status_code=400, detail=f"Menu item with id {item.menu_item_id} not found")
        
        # Verificar se o item está disponível
        if not menu_item.is_available:
            db.delete(db_order)
            db.commit()
            raise HTTPException(status_code=400, detail=f"Menu item '{menu_item.name}' is not available")
        
        # Criar o item do pedido
        db_order_item = models.OrderItem(
            order_id=db_order.id,
            menu_item_id=item.menu_item_id,
            quantity=item.quantity,
            notes=item.notes
        )
        db.add(db_order_item)
    
    db.commit()
    db.refresh(db_order)
    return db_order

@router.get("/", response_model=List[schemas.Order])
def read_orders(
    skip: int = 0, 
    limit: int = 100, 
    status: str = None,
    db: Session = Depends(get_db)
):
    query = db.query(models.Order)
    
    if status:
        query = query.filter(models.Order.status == status)
    
    orders = query.order_by(models.Order.created_at.desc()).offset(skip).limit(limit).all()
    return orders

@router.get("/{order_id}", response_model=schemas.Order)
def read_order(order_id: int, db: Session = Depends(get_db)):
    db_order = db.query(models.Order).filter(models.Order.id == order_id).first()
    if db_order is None:
        raise HTTPException(status_code=404, detail="Order not found")
    return db_order

@router.put("/{order_id}", response_model=schemas.Order)
def update_order(order_id: int, order: schemas.OrderUpdate, db: Session = Depends(get_db)):
    db_order = db.query(models.Order).filter(models.Order.id == order_id).first()
    if db_order is None:
        raise HTTPException(status_code=404, detail="Order not found")
    
    # Atualizar campos
    update_data = order.dict(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_order, key, value)
    
    db.commit()
    db.refresh(db_order)
    return db_order

@router.delete("/{order_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_order(order_id: int, db: Session = Depends(get_db)):
    db_order = db.query(models.Order).filter(models.Order.id == order_id).first()
    if db_order is None:
        raise HTTPException(status_code=404, detail="Order not found")
    
    db.delete(db_order)
    db.commit()
    return None