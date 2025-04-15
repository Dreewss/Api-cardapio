from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, Float, Table, Text
from sqlalchemy.orm import relationship

from .database import Base

# Tabela de associação entre MenuItem e Ingredient (muitos para muitos)
menu_item_ingredients = Table(
    "menu_item_ingredients",
    Base.metadata,
    Column("menu_item_id", Integer, ForeignKey("menu_items.id"), primary_key=True),
    Column("ingredient_id", Integer, ForeignKey("ingredients.id"), primary_key=True),
)

class Category(Base):
    __tablename__ = "categories"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True)
    description = Column(String, nullable=True)
    
    # Relacionamento com MenuItem
    menu_items = relationship("MenuItem", back_populates="category")

class MenuItem(Base):
    __tablename__ = "menu_items"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    description = Column(Text, nullable=True)
    price = Column(Float)
    image_url = Column(String, nullable=True)
    is_available = Column(Boolean, default=True)
    category_id = Column(Integer, ForeignKey("categories.id"))
    
    # Relacionamentos
    category = relationship("Category", back_populates="menu_items")
    ingredients = relationship("Ingredient", secondary=menu_item_ingredients, back_populates="menu_items")
    order_items = relationship("OrderItem", back_populates="menu_item")

class Ingredient(Base):
    __tablename__ = "ingredients"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True)
    is_allergen = Column(Boolean, default=False)
    
    # Relacionamento com MenuItem
    menu_items = relationship("MenuItem", secondary=menu_item_ingredients, back_populates="ingredients")

class Order(Base):
    __tablename__ = "orders"

    id = Column(Integer, primary_key=True, index=True)
    table_number = Column(Integer, nullable=True)
    customer_name = Column(String, nullable=True)
    status = Column(String, default="pending")  # pending, preparing, ready, delivered, cancelled
    created_at = Column(String)  # Armazenar como ISO string para simplicidade
    
    # Relacionamento com OrderItem
    items = relationship("OrderItem", back_populates="order")

class OrderItem(Base):
    __tablename__ = "order_items"

    id = Column(Integer, primary_key=True, index=True)
    order_id = Column(Integer, ForeignKey("orders.id"))
    menu_item_id = Column(Integer, ForeignKey("menu_items.id"))
    quantity = Column(Integer, default=1)
    notes = Column(String, nullable=True)
    
    # Relacionamentos
    order = relationship("Order", back_populates="items")
    menu_item = relationship("MenuItem", back_populates="order_items")