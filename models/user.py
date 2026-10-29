from extensions import db
from models import *

class User(db.Model):
    tablename = "__users__"
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(128), nullable=False)
    email = db.Column(db.String(128), unique=True, nullable=False)
    stock_entries = db.relationship("UserStock", back_populates="user", cascade="all, delete-orphan")
