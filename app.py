from flask import Flask, render_template, request, redirect, url_for
from extensions import db
import datetime
from models import Part, Category

app =  Flask(__name__, template_folder="templates")
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///event_database.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = True
db.init_app(app)

@app.route("/")
def hello_world():
    return "Hello world"

@app.route("/categories")
def categories():
    cats = Category.query.all()
    return render_template("categories.html", categories=cats)

@app.route("/categories/<int:cat_id>")
def category():
    return "Nothing here..."

@app.route("/stock/<int:part_id>")
def check_item(part_id):
    part = Part.query.get_or_404(part_id)
    return f"<h1>Checking {part.name}...</h1><p>Qty: X</p>"

@app.route("/login")
def login():
    return "Nothing here yet"

if __name__ == "__main__":
    with app.app_context():
        db.drop_all()
        db.create_all()
        if Part.query.count() == 0:
            for i in range(0,10):
                db.session.add(Part(name=f"Test {i}"))
        if Category.query.count() == 0:
            db.session.add(Category(name="Electronics"))
            db.session.add(Category(name="Stationery"))
            db.session.commit()   
        
        db.session.commit()    
    app.run(debug=True)
