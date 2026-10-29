from flask import Flask, render_template, request, redirect, url_for
import datetime
from models import Part, User, Category
from models.seed_db import seed_db, user_stock_test
from extensions import db

app =  Flask(__name__, template_folder="templates")
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///event_database.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = True

@app.route("/")
def hello_world():
    return render_template("base.html")

@app.route("/categories")
def categories():
    cats = Category.query.all()
    return render_template("categories.html", categories=cats)

@app.route("/categories/<int:cat_id>")
def category(cat_id):
    return render_template("category.html", category=db.session.get(Category, cat_id))

@app.route("/categories/parts/<int:part_id>")
def check_item(part_id):
    part = Part.query.get_or_404(part_id)
    return f"<h1>Checking {part.name}</h1><p>Qty: X</p>"

@app.route("/login")
def login():
    return render_template("login.html")



if __name__ == "__main__":    
    seed_db(app=app)
    #user_stock_test(app=app)
    app.run(debug=True)
