from typing import List
from . import db
from dataclasses import dataclass

@dataclass
class Product(db.Model):
    __tablename__ = 'product'
    id: int = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name: str = db.Column(db.String(100))
    price: float = db.Column(db.Numeric(precision=5, scale=2)) # price cannot exceed 999.99
    quantity: int = db.Column(db.Integer)
    vending_machine_id: int = db.Column(db.Integer, db.ForeignKey('vending_machine.id'), nullable=False)
    
@dataclass
class VendingMachine(db.Model):
    __tablename__ = 'vending_machine'
    id: int = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name: str = db.Column(db.String(100))
    location: str = db.Column(db.Text)
    products: List[Product] = db.relationship('Product', backref='vending_machine', cascade='all, delete-orphan')