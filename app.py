


from flask import Flask, render_template
from posts import get_posts

app = Flask(__name__)

@app.route("/")
def home():
    posts = get_posts()
    return render_template("home.html", posts=posts)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
