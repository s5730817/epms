from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_user, logout_user, login_required
from werkzeug.security import generate_password_hash, check_password_hash
from epms.extensions import login_manager, db
from epms.models import User

auth = Blueprint("auth", __name__)

from epms.models import User
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@auth.route("/login")
def login():
    return render_template("login.html")

@auth.route("/login", methods=["POST"])
def login_post():
    email = request.form.get("email")
    password = request.form.get("password")
    remember = True if request.form.get("remember") else False

    user = User.query.filter_by(email=email).first()

    if not user or not check_password_hash(user.password, password):
        flash("Invalid login credentials")
        return redirect(url_for("auth.login"))
    login_user(user, remember=remember)
    return redirect(url_for("app.home"))

@auth.route("/signup")
def signup():
    return render_template("signup.html")

@auth.route("/signup", methods=["POST"])
def signup_post():
    email = request.form.get("email")
    username = request.form.get("username")
    password = request.form.get("password")

    user = User.query.filter_by(email=email).first()
    if user:
        flash("Account with this email already exists")
        return redirect(url_for("auth.login"))

    new_user = User(username=username, email=email, password=generate_password_hash(password=password))
    db.session.add(new_user)
    db.session.commmit()


@auth.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("app.home"))