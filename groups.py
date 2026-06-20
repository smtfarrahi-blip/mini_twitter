from flask import Blueprint, request, session, redirect
from database import connect
import os
from werkzeug.utils import secure_filename

groups = Blueprint("groups", __name__)

UPLOAD_IMG = "uploads/images"
UPLOAD_VID = "uploads/videos"


@groups.route("/create_group", methods=["POST"])
def create_group():

    if "user" not in session:
        return redirect("/login")

    name = request.form["name"]

    db = connect()
    c = db.cursor()

    c.execute("INSERT INTO groups(name,owner) VALUES(?,?)",
              (name, session["user"]))

    c.execute("INSERT INTO group_members(group_name,username) VALUES(?,?)",
              (name, session["user"]))

    db.commit()
    db.close()

    return redirect("/")


@groups.route("/join/<name>")
def join(name):

    if "user" not in session:
        return redirect("/login")

    db = connect()
    c = db.cursor()

    c.execute("INSERT INTO group_members(group_name,username) VALUES(?,?)",
              (name, session["user"]))

    db.commit()
    db.close()

    return redirect("/")


@groups.route("/group/<name>", methods=["GET","POST"])
def group(name):

    if "user" not in session:
        return redirect("/login")

    media_path = ""

    if request.method == "POST":

        text = request.form["text"]

        file = request.files.get("media")

        if file and file.filename:

            filename = secure_filename(file.filename)

            if filename.endswith((".mp4",".mov",".avi")):
                path = os.path.join(UPLOAD_VID, filename)
                file.save(path)
                media_path = "/" + path
            else:
                path = os.path.join(UPLOAD_IMG, filename)
                file.save(path)
                media_path = "/" + path

        db = connect()
        c = db.cursor()

        c.execute("""
        INSERT INTO group_posts(group_name,username,text,media)
        VALUES(?,?,?,?)
        """, (name, session["user"], text, media_path))

        db.commit()
        db.close()

        return redirect(f"/group/{name}")

    db = connect()
    c = db.cursor()

    c.execute("""
    SELECT username,text,media FROM group_posts
    WHERE group_name=?
    ORDER BY id DESC
    """, (name,))

    posts = c.fetchall()
    db.close()

    html = f"<h2>Group: {name}</h2>"

    html += f"""
    <form method="post" enctype="multipart/form-data">
    <textarea name="text"></textarea>
    <input type="file" name="media">
    <button>ارسال</button>
    </form>
    <hr>
    """

    for p in posts:

        html += f"""
        <div>
        <b>{p[0]}</b><br>
        {p[1]}<br>
        """

        if p[2]:
            if p[2].endswith((".mp4",".mov",".avi")):
                html += f"""
                <video width="300" controls>
                <source src="{p[2]}">
                </video>
                """
            else:
                html += f"""
                <img src="{p[2]}" width="300">
                """

        html += "</div><hr>"

    return html

