from flask import Blueprint, request, session, redirect, render_template
from database import create_user, login_user

auth = Blueprint("auth", __name__)


@auth.route("/register", methods=["GET","POST"])
def register():

    if request.method == "POST":

        username = request.form["username"]
        password = request.form["password"]

        if create_user(username,password):
            session["user"] = username
            return redirect("/")

        return "این یوزرنیم قبلاً گرفته شده"

    return render_template("register.html")



@auth.route("/login", methods=["GET","POST"])
def login():

    if request.method == "POST":

        username = request.form["username"]
        password = request.form["password"]


        if login_user(username,password):
            session["user"] = username
            return redirect("/")


        return "یوزرنیم یا رمز اشتباه است"


    return render_template("login.html")



@auth.route("/logout")
def logout():

    session.clear()
    return redirect("/login")
