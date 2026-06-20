from flask import Flask, render_template_string, request, redirect, session
import os, json, uuid
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.secret_key = "zgrom"

UPLOAD = "uploads"
os.makedirs(UPLOAD, exist_ok=True)

def load(f):
    return json.load(open(f,"r",encoding="utf-8")) if os.path.exists(f) else []

def save(f,d):
    open(f,"w",encoding="utf-8").write(json.dumps(d,ensure_ascii=False,indent=2))

UI = """
<!DOCTYPE html>
<html>
<head>
<meta name="viewport" content="width=device-width, initial-scale=1">
<style>
body{margin:0;font-family:sans-serif;background:linear-gradient(135deg,#0f172a,#312e81);color:white}
.box{background:rgba(255,255,255,0.12);backdrop-filter:blur(15px);margin:10px;padding:15px;border-radius:18px}
input,textarea,button{width:100%%;padding:10px;margin-top:8px;border-radius:12px;border:none}
button{background:#6366f1;color:white}
img{max-width:100%%;border-radius:15px}
a{color:#93c5fd}
.nav{display:flex;justify-content:space-around;padding:10px;background:rgba(0,0,0,0.3);position:sticky;top:0}
</style>
</head>

<body>

<div class="nav">
<a href="/">🏠</a>
<a href="/profile">👤</a>
<a href="/dm">💬</a>
<a href="/logout">🚪</a>
</div>

<div style="padding:10px">
%s
</div>

</body>
</html>
"""

@app.route("/login",methods=["GET","POST"])
def login():
    if request.method=="POST":
        session["u"]=request.form["u"]
        return redirect("/")
    return UI % """
    <div class='box'>
    <h2>ورود Zgrom</h2>
    <form method='post'>
    <input name='u' placeholder='username'>
    <button>ورود</button>
    </form>
    </div>
    """

@app.route("/logout")
def logout():
    session.clear()
    return redirect("/login")


@app.route("/",methods=["GET","POST"])
def home():

    if "u" not in session:
        return redirect("/login")

    posts=load("posts.json")

    if request.method=="POST":

        img=""

        if "img" in request.files:
            f=request.files["img"]
            if f.filename:
                name=secure_filename(f.filename)
                path=os.path.join(UPLOAD,name)
                f.save(path)
                img="/"+path

        posts.insert(0,{
            "id":str(uuid.uuid4()),
            "u":session["u"],
            "text":request.form["text"],
            "img":img,
            "likes":0,
            "dislikes":0
        })

        save("posts.json",posts)
        return redirect("/")


    html=f"<div class='box'>سلام {session['u']}</div>"

    for i,p in enumerate(posts):

        html+=f"""
        <div class='box'>
        <b>{p['u']}</b><br>
        {p['text']}<br>
        {"<img src='"+p['img']+"'>" if p['img'] else ""}
        <br>
        ❤️ {p['likes']}
        </div>
        """

    html+="""
    <div class='box'>
    <form method='post' enctype='multipart/form-data'>
    <textarea name='text'></textarea>
    <input type='file' name='img'>
    <button>post</button>
    </form>
    </div>
    """

    return UI % html


@app.route("/like/<int:i>")
def like(i):
    p=load("posts.json")
    p[i]["likes"]+=1
    save("posts.json",p)
    return redirect("/")


@app.route("/profile")
def profile():

    if "u" not in session:
        return redirect("/login")

    posts=load("posts.json")
    me=session["u"]

    html=f"<div class='box'><h2>{me}</h2></div>"

    for p in posts:
        if p["u"]==me:
            html+=f"<div class='box'>{p['text']}</div>"

    return UI % html


if __name__=="__main__":
    app.run(host="0.0.0.0",port=5000)
