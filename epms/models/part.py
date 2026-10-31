from epms.extensions import db
from epms.models import *
from sqlalchemy import ForeignKey

class Part(db.Model):
    __tablename__ = "parts"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128), unique=False, nullable=False)
    cat_id = db.Column(db.Integer, ForeignKey("categories.id"), nullable=False)
    category = db.relationship("Category", back_populates="parts")
    stock_entries = db.relationship("UserStock", back_populates="part")
    