from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_user, logout_user, login_required
from werkzeug.security import generate_password_hash, check_password_hash
from epms.extensions import login_manager, db
from epms.models import User

auth = Blueprint("auth", __name__)

@login_manager.user_loader
def load_user(user_id):
    try:
        return User.query.get(int(user_id))
    except:
        print("Couldn't load user")
        flash("Couldn't load user")
        return redirect(url_for("auth.login"))

@auth.route("/login")
def login():
    return render_template("login.html")

@auth.route("/")
def start():
    return redirect(url_for("auth.login"))


@auth.route("/login", methods=["POST"])
def login_post():
    email = request.form.get("email")
    password = request.form.get("password")
    remember = True if request.form.get("remember") else False
    user = User.query.filter_by(email=email).first()
    print(user)
    if not user or not check_password_hash(user.password, password):
        flash("Invalid login credentials")
        return redirect(url_for("auth.login"))
    login_user(user, remember=remember)
    return redirect(url_for("main.categories"))

@auth.route("/signup", methods=["GET"])
def signup():
    return render_template("signup.html")

@auth.route("/signup", methods=["POST"])
def signup_post():
    email = request.form.get("email")
    username = request.form.get("username")
    password = request.form.get("password")
    print(password)
    user = User.query.filter_by(email=email).first()
    if user:
        print("Account with this email already exists")
        flash("Account with this email already exists")
        return redirect(url_for("auth.login"))

    new_user = User(username=username, email=email, password=generate_password_hash(password=password))
    print("Account created")
    print(new_user)
    db.session.add(new_user)
    db.session.commit()

    return redirect(url_for("auth.login"))

@auth.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("auth.login"))