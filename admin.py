from flask import Blueprint, session, request
from database import connect

admin = Blueprint("admin", __name__)


@admin.route("/admin")
def panel():

    if "user" not in session:
        return "login first"


    db = connect()
    c = db.cursor()


    c.execute(
    "SELECT admin FROM users WHERE username=?",
    (session["user"],)
    )

    result=c.fetchone()


    if not result or result[0] != 1:
        return "access denied"


    c.execute(
    "SELECT username,verified FROM users"
    )

    users=c.fetchall()


    html="<h1>Admin Panel</h1>"


    for u in users:

        html+=f"""
        <p>
        {u[0]}
        -
        verified: {u[1]}

        <a href="/verify/{u[0]}">
        give blue tick
        </a>

        </p>
        """


    db.close()

    return html



@admin.route("/verify/<user>")
def verify(user):

    if "user" not in session:
        return "login first"


    db=connect()
    c=db.cursor()


    c.execute(
    "SELECT admin FROM users WHERE username=?",
    (session["user"],)
    )

    me=c.fetchone()


    if not me or me[0] != 1:
        return "access denied"


    c.execute(
    "UPDATE users SET verified=1 WHERE username=?",
    (user,)
    )


    db.commit()
    db.close()


    return "verified"

