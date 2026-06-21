from flask import Blueprint, request, redirect, render_template
import sqlite3

posts = Blueprint("posts", __name__)


@posts.route("/post", methods=["POST"])
def create_post():

    text = request.form.get("text")
    username = "user"

    conn = sqlite3.connect("zgrom.db")
    c = conn.cursor()

    c.execute(
        "INSERT INTO posts(username,text,likes) VALUES(?,?,?)",
        (username,text,0)
    )

    conn.commit()
    conn.close()

    return redirect("/")


@posts.route("/posts")
def show_posts():

    conn = sqlite3.connect("zgrom.db")
    c = conn.cursor()

    c.execute(
        "SELECT username,text,image,likes FROM posts"
    )

    data = c.fetchall()

    conn.close()

    return render_template(
        "index.html",
        posts=data
    )

