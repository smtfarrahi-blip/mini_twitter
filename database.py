import sqlite3


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
        password TEXT
    )
    """)


    c.execute("""
    CREATE TABLE IF NOT EXISTS posts(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user TEXT,
        text TEXT,
        img TEXT,
        likes INTEGER DEFAULT 0,
        dislikes INTEGER DEFAULT 0
    )
    """)


    c.execute("""
    CREATE TABLE IF NOT EXISTS messages(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        sender TEXT,
        receiver TEXT,
        text TEXT
    )
    """)


    c.execute("""
    CREATE TABLE IF NOT EXISTS groups(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT,
        owner TEXT
    )
    """)


    c.execute("""
    CREATE TABLE IF NOT EXISTS group_members(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        group_name TEXT,
        username TEXT
    )
    """)


    c.execute("""
    CREATE TABLE IF NOT EXISTS group_posts(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        group_name TEXT,
        username TEXT,
        text TEXT,
        media TEXT
    )
    """)


    db.commit()
    db.close()
