import sqlite3
from werkzeug.security import generate_password_hash, check_password_hash

DB = "zgrom.db"


def connect():
    return sqlite3.connect(DB)


def init_db():
    db = connect()
    c = db.cursor()

    c.execute("""
    CREATE TABLE IF NOT EXISTS users(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE,
        password TEXT,
        admin INTEGER DEFAULT 0,
        verified INTEGER DEFAULT 0
    )
    """)

    c.execute("""
    CREATE TABLE IF NOT EXISTS posts(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT,
        text TEXT,
        image TEXT,
        likes INTEGER DEFAULT 0
    )
    """)

    c.execute("""
    CREATE TABLE IF NOT EXISTS messages(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        sender TEXT,
        receiver TEXT,
        message TEXT
    )
    """)

    db.commit()
    db.close()


def create_user(username,password):

    db=connect()
    c=db.cursor()

    try:
        c.execute(
        "INSERT INTO users(username,password) VALUES(?,?)",
        (
        username,
        generate_password_hash(password)
        ))

        db.commit()
        return True

    except:
        return False


def login_user(username,password):

    db=connect()
    c=db.cursor()

    c.execute(
    "SELECT password FROM users WHERE username=?",
    (username,)
    )

    user=c.fetchone()
    db.close()

    if user:
        return check_password_hash(user[0],password)

    return False
