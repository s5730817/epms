from flask import Blueprint, render_template
from epms.models import *
from epms.extensions import db
from flask_login import current_user, login_required

main_bp = Blueprint("main", __name__)

"""
@main_bp.route("/")
@login_required
def hello():
    return render_template("base.html")
"""

@main_bp.route("/categories")
@login_required
def categories():
    cats = Category.query.all()
    return render_template("categories.html", categories=cats)


@main_bp.route("/categories/<int:cat_id>")
@login_required
def category(cat_id):
    user = User.query.get_or_404(current_user.id)
    user_category_parts = Part.query.filter(Part.id.in_([stock_item.part_id for stock_item in UserStock.query.filter_by(user_id=current_user.id).all()])).filter_by(cat_id=cat_id).all()    
    return render_template("display_user.html", user=user, user_category_parts=user_category_parts)
    

@main_bp.route("/categories/parts/<int:part_id>")
@login_required
def check_item(part_id):
    part = Part.query.get_or_404(part_id)
    return f"<h1>Checking {part.name}</h1><p>Qty: X</p>"
