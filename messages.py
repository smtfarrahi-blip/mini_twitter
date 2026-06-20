from flask import Blueprint, request, session, redirect
from database import connect

messages = Blueprint("messages", __name__)


@messages.route("/dm/<user>", methods=["GET","POST"])
def dm(user):

    if "user" not in session:
        return redirect("/login")

    db = connect()
    c = db.cursor()

    if request.method=="POST":

        text=request.form["message"]

        c.execute(
        "INSERT INTO messages(sender,receiver,message) VALUES(?,?,?)",
        (
        session["user"],
        user,
        text
        ))

        db.commit()


    c.execute(
    """
    SELECT sender,message 
    FROM messages
    WHERE 
    (sender=? AND receiver=?)
    OR
    (sender=? AND receiver=?)
    """,
    (
    session["user"],
    user,
    user,
    session["user"]
    ))

    chats=c.fetchall()

    db.close()


    html=f"<h2>DM با {user}</h2>"


    for m in chats:
        html+=f"""
        <p>
        <b>{m[0]}:</b>
        {m[1]}
        </p>
        """


    html+="""
    <form method="post">

    <input name="message">

    <button>
    ارسال
    </button>

    </form>
    """

    return html
