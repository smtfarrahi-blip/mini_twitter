from flask import Flask, session, redirect
from database import init_db
from auth import auth
from posts import posts
from messages import messages
from admin import admin


app = Flask(__name__)

app.secret_key = "zgrom_secret_key"


init_db(from groups import groups
app.register_blueprint(groups) )


app.register_blueprint(auth)
app.register_blueprint(posts)
app.register_blueprint(messages)
app.register_blueprint(admin)



@app.route("/make_admin")
def make_admin():

    if "user" not in session:
        return redirect("/login")


    from database import connect

    db=connect()
    c=db.cursor()


    c.execute(
    "UPDATE users SET admin=1 WHERE username=?",
    (session["user"],)
    )


    db.commit()
    db.close()


    return "You are admin now 🔵"



@app.route("/profile")
def profile():

    if "user" not in session:
        return redirect("/login")

    from database import connect

    db=connect()
    c=db.cursor()

    c.execute(
    "SELECT verified FROM users WHERE username=?",
    (session["user"],)
    )

    v=c.fetchone()

    db.close()


    tick=" 🔵" if v and v[0]==1 else ""

    return f"""
    <h1>
    {session['user']}{tick}
    </h1>

    <a href="/">home</a>
    """


if __name__=="__main__":

    app.run(
    host="0.0.0.0",
    port=5000
    )
