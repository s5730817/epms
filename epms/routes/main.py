from flask import Blueprint, render_template
from epms.models import *
from epms.extensions import db

main_bp = Blueprint("main", __name__)

@main_bp.route("/")
def hello():
    return render_template("base.html")


@main_bp.route("/categories")
def categories():
    cats = Category.query.all()
    return render_template("categories.html", categories=cats)


@main_bp.route("/categories/<int:cat_id>")
def category(cat_id):
    return render_template("category.html", category=db.session.get(Category, cat_id))


@main_bp.route("/categories/parts/<int:part_id>")
def check_item(part_id):
    part = Part.query.get_or_404(part_id)
    return f"<h1>Checking {part.name}</h1><p>Qty: X</p>"

    
@main_bp.route("/home/<int:user_id>")
def display_user(user_id):
    user = User.query.get_or_404(user_id)
    user_stock = Part.query.filter(Part.id.in_([stock_item.part_id for stock_item in UserStock.query.filter_by(user_id=user_id).all()])).all()    
    return render_template("display_user.html", user=user, user_stock=user_stock)
