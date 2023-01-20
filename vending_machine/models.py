from . import db
from dataclasses import dataclass

@dataclass
class VendingMachine(db.Model):
    __tablename__ = 'vending_machine'
    id: int = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name: str = db.Column(db.String(100))
    location: str = db.Column(db.Text)