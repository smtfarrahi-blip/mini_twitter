from flask import Flask, session, redirect
from database import init_db

from auth import auth
from posts import posts
from messages import messages
from admin import admin
from groups import groups

app = Flask(__name__)

app.secret_key = "zgrom_secret_key"

# دیتابیس فقط یکبار
init_db()

# ثبت بلوپرینت‌ها
app.register_blueprint(auth)
app.register_blueprint(posts)
app.register_blueprint(messages)
app.register_blueprint(admin)
app.register_blueprint(groups)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
