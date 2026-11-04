from epms.extensions import db
from epms.models import *
from flask_login import UserMixin
from epms.extensions import login_manager

@login_manager.user_loader
def get_user(id):
    return User.query.get(int(id))

class User(db.Model, UserMixin):
    tablename = "__users__"
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(128), nullable=False)
    email = db.Column(db.String(128), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)
    stock_entries = db.relationship("UserStock", back_populates="user", cascade="all, delete-orphan")