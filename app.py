from flask import Flask, render_template, request, redirect
from posts import posts
from auth import auth
from groups import groups

app = Flask(__name__)

app.secret_key = "zweez_secret"

app.register_blueprint(auth)
app.register_blueprint(posts)
app.register_blueprint(groups)


@app.route("/")
def home():
    return render_template("index.html")


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
