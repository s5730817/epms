from extensions import db
from models import *
from sqlalchemy import ForeignKey

class UserStock(db.Model):
    user_id = db.Column(db.Integer, ForeignKey("user.id"), primary_key=True)
    part_id = db.Column(db.Integer, ForeignKey("parts.id"), primary_key=True)
    quantity = db.Column(db.Integer, nullable=False, default=0)

    user = db.relationship("User", back_populates="stock_entries")
    part = db.relationship("Part", back_populates="stock_entries")