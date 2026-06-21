from flask import Flask, render_template, request, redirect, session, send_from_directory
import os
import sqlite3

app = Flask(__name__)
app.secret_key = "secret"

UPLOAD_FOLDER = "uploads"
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER


# ---------------- DB ----------------
def get_db():
    conn = sqlite3.connect("zgrom.db")
    return conn


# ---------------- HOME ----------------
@app.route("/")
def home():
    conn = get_db()
    c = conn.cursor()
    c.execute("SELECT username, text, image, likes FROM posts ORDER BY id DESC")
    posts = c.fetchall()
    conn.close()
    return render_template("index.html", posts=posts)


# ---------------- UPLOAD FILES ----------------
@app.route("/uploads/<filename>")
def uploaded_file(filename):
    return send_from_directory(app.config["UPLOAD_FOLDER"], filename)


# ---------------- LOGIN SIMPLE ----------------
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        session["user"] = request.form["username"]
        return redirect("/")
    return render_template("login.html")


# ---------------- POST CREATE ----------------
@app.route("/post", methods=["POST"])
def post():
    if "user" not in session:
        return redirect("/login")

    text = request.form["text"]
    image = request.files.get("image")

    filename = None

    if image:
        filename = image.filename
        image.save(os.path.join(app.config["UPLOAD_FOLDER"], filename))

    conn = get_db()
    c = conn.cursor()
    c.execute(
        "INSERT INTO posts (username, text, image, likes) VALUES (?, ?, ?, 0)",
        (session["user"], text, filename),
    )
    conn.commit()
    conn.close()

    return redirect("/")


# ---------------- RUN ----------------
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
