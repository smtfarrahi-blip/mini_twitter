from flask import Flask, request, redirect, render_template_string

app = Flask(__name__)

users = {}
posts = []
follows = []
current_user = None


STYLE = """
<style>
body{
font-family:sans-serif;
background:linear-gradient(135deg,#111827,#312e81);
color:white;
padding:20px;
}

.box{
background:rgba(255,255,255,0.12);
backdrop-filter:blur(12px);
border-radius:20px;
padding:20px;
margin:15px;
}

input,button{
padding:10px;
border-radius:10px;
border:none;
margin:5px;
}

button{
background:#6366f1;
color:white;
}

img{
border-radius:15px;
max-width:250px;
}
a{
color:#93c5fd;
}
</style>
"""


@app.route("/")
def home():
    if not current_user:
        return redirect("/login")

    html = STYLE + """
    <div class="box">
    <h1>ناراستی 😏</h1>

    سلام {{user}}

    <br>
    <a href="/profile/{{user}}">پروفایل من</a>
    |
    <a href="/logout">خروج</a>

    </div>


    <div class="box">

    <form method="POST" action="/post">

    <input name="text" placeholder="چی تو سرته؟">

    <input name="image" placeholder="لینک عکس">

    <button>ارسال</button>

    </form>

    </div>


    {% for p in posts %}

    <div class="box">

    <b>{{p.user}}</b>

    <p>{{p.text}}</p>

    {% if p.image %}
    <img src="{{p.image}}">
    {% endif %}

    <br>

    ❤️ {{p.like}}
    💔 {{p.dislike}}

    <br>

    <a href="/like/{{p.id}}">لایک</a>
    |
    <a href="/dislike/{{p.id}}">دیس‌لایک</a>

    </div>

    {% endfor %}
    """

    return render_template_string(
        html,
        user=current_user,
        posts=posts
    )



@app.route("/login",methods=["GET","POST"])
def login():

    global current_user

    if request.method=="POST":

        u=request.form["username"]

        if u not in users:

            users[u]={
            "bio":"",
            "avatar":"",
            "header":""
            }

        current_user=u

        return redirect("/")


    return STYLE+"""
    <div class="box">

    <h2>ورود</h2>

    <form method="POST">

    <input name="username">

    <button>ورود</button>

    </form>

    </div>
    """



@app.route("/profile/<name>",methods=["GET","POST"])
def profile(name):

    if name not in users:
        return "کاربر پیدا نشد"


    if request.method=="POST":

        users[name]["bio"]=request.form["bio"]
        users[name]["avatar"]=request.form["avatar"]
        users[name]["header"]=request.form["header"]

        return redirect("/profile/"+name)



    followers=follows.count(name)

    following=follows.count(current_user)



    return render_template_string(
    STYLE+"""

    <div class="box">

    {% if user.header %}
    <img src="{{user.header}}">
    {% endif %}

    <h1>{{name}}</h1>


    {% if user.avatar %}
    <img src="{{user.avatar}}">
    {% endif %}


    <p>{{user.bio}}</p>


    <p>
    دنبال‌کننده: {{followers}}
    دنبال‌شونده: {{following}}
    </p>


    {% if name==current %}

    <form method="POST">

    <input name="bio" placeholder="بیو">

    <input name="avatar" placeholder="عکس پروفایل">

    <input name="header" placeholder="هدر">

    <button>ذخیره</button>

    </form>

    {% else %}

    <a href="/follow/{{name}}">
    دنبال کردن
    </a>

    {% endif %}


    </div>

    <a href="/">برگشت</a>

    """,
    name=name,
    user=users[name],
    current=current_user,
    followers=followers,
    following=following
    )



@app.route("/post",methods=["POST"])
def post():

    posts.append({

    "id":len(posts),

    "user":current_user,

    "text":request.form["text"],

    "image":request.form["image"],

    "like":0,

    "dislike":0

    })

    return redirect("/")



@app.route("/like/<int:id>")
def like(id):

    posts[id]["like"]+=1

    return redirect("/")



@app.route("/dislike/<int:id>")
def dislike(id):

    posts[id]["dislike"]+=1

    return redirect("/")



@app.route("/follow/<name>")
def follow(name):

    if name not in follows:

        follows.append(name)

    return redirect("/profile/"+name)



@app.route("/logout")
def logout():

    global current_user

    current_user=None

    return redirect("/login")



app.run(host="0.0.0.0",port=5000)
