from flask import Blueprint, render_template, request, redirect, url_for
from epms.models import *
from epms.extensions import db, mongo_client
from epms.modules.pdf_extract import *
from epms.modules.llm_parse import *
from flask_login import current_user, login_required
from werkzeug.utils import secure_filename
import os
import json

main_bp = Blueprint("main", __name__)
mongo_db = mongo_client["epms"]
collection = mongo_db["parts"]

"""
@main_bp.route("/")
@login_required
def hello():
    return render_template("base.html")
"""

@main_bp.route("/categories")
@login_required
def get_categories():
    cats = Category.query.all()
    return render_template("categories.html", categories=cats)


@main_bp.route("/categories/<int:cat_id>")
@login_required
def get_category(cat_id):
    user = User.query.get_or_404(current_user.id)
    user_category_parts_query = (
        db.select(Part, UserStock.quantity)
        .join(UserStock, UserStock.part_id == Part.id)
        .where(UserStock.user_id == current_user.id, Part.cat_id == cat_id)
    )

    user_category_parts = db.session.execute(user_category_parts_query).all()    
    return render_template("display_user.html", user=user, user_category_parts=user_category_parts)
    

@main_bp.route("/categories/part/<int:part_id>")
@login_required
def get_item(part_id):

    part_query = (
            db.select(Part.id, Part.name, Part.doc_link, UserStock.quantity)
            .join(UserStock, UserStock.part_id == Part.id)
            .where(UserStock.user_id == current_user.id, Part.id == part_id)
        )
    part_data_file = collection.find_one({"part_id": {"$eq": part_id}})
    part_data = part_data_file["data"] if part_data_file is not None else None
    part_data_json = json.loads(part_data)    
    part = db.session.execute(part_query).first()

    return render_template("part.html", part=part, part_data=part_data_json)


@main_bp.route("/change_qtt", methods=["POST"])
def update_part_qtt():
    new_qtt = int(request.form.get("new_qtt"))
    part_id = int(request.form.get("part_id"))
    entry = db.session.get(UserStock, (current_user.id, part_id))
    entry.quantity = new_qtt
    db.session.commit()
    return redirect(url_for("main.get_item", part_id=part_id))


@main_bp.route("/add_part", methods=["GET"])
@login_required
def add_part():
    categories = db.session.execute(db.select(Category).order_by(Category.name)).scalars()
    # This is to check if part with same name already exists
    """parts = db.session.execute(db.select(Part.name)).scalars()"""
    return render_template("add_part.html", categories=categories)


@main_bp.route("/add_part", methods=["POST"])
@login_required
def add_part_post():
    name = request.form.get("name")
    quantity = request.form.get("quantity")
    doc_link = request.form.get("doc-link")
    cat_id = request.form.get("category")
    part = Part(
        name=name,
        doc_link=doc_link,
        cat_id=cat_id
    )

    db.session.add(part)
    db.session.flush()

    stock_entry = UserStock(
        user_id=current_user.id, 
        part_id=part.id, 
        quantity=quantity
    )
    print(f"Part {part.id} added by user {current_user.id}, quantity: {stock_entry.quantity}")
    db.session.add(stock_entry)
    db.session.commit()
    return redirect(url_for("main.categories"))


@main_bp.route("/update_datasheet", methods=["POST"])
@login_required
def update_datasheet():
    UPLOAD_FOLDER = os.path.join(os.path.dirname(os.path.abspath(__file__)), "uploads")
    os.makedirs(UPLOAD_FOLDER, exist_ok=True)
    file = request.files.get("part_datasheet")
    if file and file.filename:
        filepath = os.path.join(UPLOAD_FOLDER, secure_filename(file.filename))
        file.save(filepath)
    with pdfplumber.open(filepath) as pdf:
        print(check_pdf_type(pdf))
        text = extract_text(pdf)
        data = ""
        for page in text:
            data += page["text"]
        part_datasheet = parse_datasheet(data)

        part_id = request.args.get("part_id", None)
        try:
            part_id = int(part_id)
        except:
            print("Something aint right bro")

        part_data = {
            "part_id": part_id,
            "data": part_datasheet  
        }

        query_filter = {"part_id": part_id}
        update_operation = {"$set": {"data":part_data}}
        collection.update_one(query_filter, update_operation)
        
    return redirect(url_for("main.categories"))


@main_bp.route("/upload_datasheet", methods=["POST"])
@login_required
def upload_datasheet():
    UPLOAD_FOLDER = os.path.join(os.path.dirname(os.path.abspath(__file__)), "uploads")
    os.makedirs(UPLOAD_FOLDER, exist_ok=True)
    file = request.files.get("part_datasheet")
    if file and file.filename:
        filepath = os.path.join(UPLOAD_FOLDER, secure_filename(file.filename))
        file.save(filepath)
    with pdfplumber.open(filepath) as pdf:
        print(check_pdf_type(pdf))
        text = extract_text(pdf)
        data = ""
        for page in text:
            data += page["text"]
        part_datasheet = parse_datasheet(data)

        part_id = request.args.get("part_id", None)
        try:
            part_id = int(part_id)
        except:
            print("Something aint right bro")

        part_data = {
            "part_id": part_id,
            "data": part_datasheet  
        }
        collection.insert_one(part_data)
        
    return redirect(url_for("main.categories"))

