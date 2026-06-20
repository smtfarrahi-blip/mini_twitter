from flask import Blueprint, request, session, redirect, render_template
from database import connect

auth = Blueprint("auth", __name__)


# ---------------- REGISTER ----------------
@auth.route("/register", methods=["GET","POST"])
def register():

    if request.method == "POST":

        username = request.form["username"]
        password = request.form["password"]

        db = connect()
        c = db.cursor()

        # چک تکراری بودن
        c.execute("SELECT username FROM users WHERE username=?", (username,))
        exists = c.fetchone()

        if exists:
            db.close()
            return "این یوزرنیم قبلاً گرفته شده 😅"

        c.execute(
            "INSERT INTO users(username,password,admin,verified) VALUES(?,?,0,0)",
            (username, password)
        )

        db.commit()
        db.close()

        session["user"] = username
        return redirect("/")

    return render_template("register.html")


# ---------------- LOGIN ----------------
@auth.route("/login", methods=["GET","POST"])
def login():

    if request.method == "POST":

        username = request.form["username"]
        password = request.form["password"]

        db = connect()
        c = db.cursor()

        c.execute(
            "SELECT username FROM users WHERE username=? AND password=?",
            (username, password)
        )

        user = c.fetchone()
        db.close()

        if user:
            session["user"] = username
            return redirect("/")

        return "یوزرنیم یا رمز اشتباهه 😄"

    return render_template("login.html")


# ---------------- LOGOUT ----------------
@auth.route("/logout")
def logout():
    session.clear()
    return redirect("/login")
