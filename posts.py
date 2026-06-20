from flask import Blueprint, request, session, redirect, render_template
from database import connect
import uuid
import os
from werkzeug.utils import secure_filename

posts = Blueprint("posts", __name__)

UPLOAD = "uploads/images"


@posts.route("/", methods=["GET","POST"])
def home():

    if "user" not in session:
        return redirect("/login")

    db = connect()
    c = db.cursor()

    # ارسال پست
    if request.method == "POST":

        text = request.form["text"]
        img = ""

        file = request.files.get("img")

        if file and file.filename:

            filename = secure_filename(file.filename)
            path = os.path.join(UPLOAD, filename)
            file.save(path)
            img = "/" + path

        c.execute("""
        INSERT INTO posts(user,text,img,likes,dislikes)
        VALUES(?,?,?,?,?)
        """, (session["user"], text, img, 0, 0))

        db.commit()

    # گرفتن پست‌ها
    c.execute("SELECT user,text,img,likes,dislikes FROM posts ORDER BY id DESC")
    post_rows = c.fetchall()

    posts_list = []
    for p in post_rows:
        posts_list.append({
            "user": p[0],
            "text": p[1],
            "img": p[2],
            "likes": p[3],
            "dislikes": p[4]
        })

    # گرفتن گروه‌ها
    c.execute("SELECT name FROM groups")
    groups_rows = c.fetchall()

    groups_list = []
    for g in groups_rows:
        groups_list.append({"name": g[0]})

    db.close()

    return render_template(
        "home.html",
        user=session["user"],
        posts=posts_list,
        groups=groups_list
    )
