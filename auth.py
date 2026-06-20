from flask import Blueprint, request, session, redirect
from database import create_user, login_user

auth = Blueprint("auth", __name__)


@auth.route("/register", methods=["GET","POST"])
def register():

    if request.method=="POST":

        username=request.form["username"]
        password=request.form["password"]

        if create_user(username,password):
            session["user"]=username
            return redirect("/")

        return "username already exists"

    return """
    <h2>ثبت نام Zgrom</h2>

    <form method="post">

    <input name="username" placeholder="username">

    <input name="password" placeholder="password" type="password">

    <button>
    ثبت نام
    </button>

    </form>
    """


@auth.route("/login", methods=["GET","POST"])
def login():

    if request.method=="POST":

        username=request.form["username"]
        password=request.form["password"]

        if login_user(username,password):
            session["user"]=username
            return redirect("/")

        return "wrong username or password"


    return """
    <h2>ورود Zgrom</h2>

    <form method="post">

    <input name="username">

    <input name="password" type="password">

    <button>
    ورود
    </button>

    </form>

    """


@auth.route("/logout")
def logout():

    session.clear()
    return redirect("/login")
