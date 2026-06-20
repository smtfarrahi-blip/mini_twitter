from flask import Blueprint, request, session, redirect
from database import connect

posts = Blueprint("posts", __name__)


@posts.route("/post", methods=["POST"])
def create_post():

    if "user" not in session:
        return redirect("/login")

    text = request.form["text"]

    db = connect()
    c = db.cursor()

    c.execute(
        "INSERT INTO posts(username,text) VALUES(?,?)",
        (session["user"], text)
    )

    db.commit()
    db.close()

    return redirect("/")


@posts.route("/")
def home():

    db = connect()
    c = db.cursor()

    c.execute(
        "SELECT username,text FROM posts ORDER BY id DESC"
    )

    data = c.fetchall()

    db.close()

    html = ""

    for p in data:
        html += f"""
        <div>
        <b>{p[0]}</b>
        <br>
        {p[1]}
        </div>
        <hr>
        """

    return f"""
    <h1>Zgrom</h1>

    <a href="/logout">خروج</a>

    <form action="/post" method="post">
    <textarea name="text"></textarea>
    <button>ارسال</button>
    </form>

    {html}
    """

