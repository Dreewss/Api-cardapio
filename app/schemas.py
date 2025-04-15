from typing import List, Optional
from pydantic import BaseModel
from datetime import datetime

# Ingredient schemas
class IngredientBase(BaseModel):
    name: str
    is_allergen: bool = False

class IngredientCreate(IngredientBase):
    pass

class Ingredient(IngredientBase):
    id: int

    class Config:
        orm_mode = True

# Category schemas
class CategoryBase(BaseModel):
    name: str
    description: Optional[str] = None

class CategoryCreate(CategoryBase):
    pass

class Category(CategoryBase):
    id: int

    class Config:
        orm_mode = True

# MenuItem schemas
class MenuItemBase(BaseModel):
    name: str
    description: Optional[str] = None
    price: float
    image_url: Optional[str] = None
    is_available: bool = True
    category_id: int

class MenuItemCreate(MenuItemBase):
    ingredient_ids: List[int] = []

class MenuItemUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    price: Optional[float] = None
    image_url: Optional[str] = None
    is_available: Optional[bool] = None
    category_id: Optional[int] = None
    ingredient_ids: Optional[List[int]] = None

class MenuItem(MenuItemBase):
    id: int
    category: Category
    ingredients: List[Ingredient] = []

    class Config:
        orm_mode = True

# OrderItem schemas
class OrderItemBase(BaseModel):
    menu_item_id: int
    quantity: int = 1
    notes: Optional[str] = None

class OrderItemCreate(OrderItemBase):
    pass

class OrderItem(OrderItemBase):
    id: int
    menu_item: MenuItem

    class Config:
        orm_mode = True

# Order schemas
class OrderBase(BaseModel):
    table_number: Optional[int] = None
    customer_name: Optional[str] = None
    status: str = "pending"

class OrderCreate(OrderBase):
    items: List[OrderItemCreate]

class OrderUpdate(BaseModel):
    table_number: Optional[int] = None
    customer_name: Optional[str] = None
    status: Optional[str] = None

class Order(OrderBase):
    id: int
    created_at: str
    items: List[OrderItem] = []

    class Config:
        orm_mode = True