from flask import Blueprint, request, session, redirect
from database import connect
import os
from werkzeug.utils import secure_filename

posts = Blueprint("posts", __name__)

UPLOAD_IMG = "uploads/images"
UPLOAD_VID = "uploads/videos"


@posts.route("/", methods=["GET","POST"])
def home():

    if "user" not in session:
        return redirect("/login")

    if request.method == "POST":

        text = request.form.get("text","")

        file = request.files.get("media")
        media = ""

        if file and file.filename:

            filename = secure_filename(file.filename)

            if filename.endswith((".mp4",".mov",".avi")):
                path = os.path.join(UPLOAD_VID, filename)
            else:
                path = os.path.join(UPLOAD_IMG, filename)

            os.makedirs(os.path.dirname(path), exist_ok=True)

            file.save(path)

            media = "/" + path


        db = connect()
        c = db.cursor()

        c.execute("""
        INSERT INTO posts(username,text,image,likes)
        VALUES(?,?,?,?)
        """,
        (
            session["user"],
            text,
            media,
            0
        ))

        db.commit()
        db.close()

        return redirect("/")


    db = connect()
    c = db.cursor()

    c.execute("""
    SELECT username,text,image,likes
    FROM posts
    ORDER BY id DESC
    """)

    data = c.fetchall()
    db.close()


    html = """
    <style>

    body{
    background:#050505;
    color:white;
    font-family:sans-serif;
    }

    .card{
    background:rgba(255,255,255,0.08);
    backdrop-filter:blur(15px);
    border-radius:20px;
    padding:20px;
    margin:15px;
    border:1px solid rgba(255,255,255,0.2);
    }

    .logo{
    color:#ffd400;
    font-size:30px;
    }

    </style>

    <h1 class="logo">🐝 Zweez</h1>

    <form method="post" enctype="multipart/form-data"
    class="card">

    <textarea name="text"
    placeholder="پیام جدید..."
    style="width:100%;height:80px;"></textarea>

    <input type="file" name="media">

    <button>
    ارسال 🐝
    </button>

    </form>
    """


    for p in data:

        html += f"""
        <div class="card">

        <b style="color:#ffd400">
        🐝 {p[0]}
        </b>

        <br><br>

        {p[1]}

        <br>
        """

        if p[2]:

            if p[2].endswith(
            (".mp4",".mov",".avi")):

                html += f"""
                <video width="300" controls>
                <source src="{p[2]}">
                </video>
                """

            else:

                html += f"""
                <img src="{p[2]}"
                width="300"
                style="border-radius:15px;">
                """


        html += f"""

        <br>
        💛 {p[3]}

        </div>

        """


    return html






