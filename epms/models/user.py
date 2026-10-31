from epms.extensions import db
from epms.models import *

class User(db.Model):
    tablename = "__users__"
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(128), nullable=False)
    email = db.Column(db.String(128), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False, default="1234")
    stock_entries = db.relationship("UserStock", back_populates="user", cascade="all, delete-orphan")
