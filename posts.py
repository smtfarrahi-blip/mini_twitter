import sqlite3

def get_posts():
    conn = sqlite3.connect("zgrom.db")
    c = conn.cursor()

    c.execute("SELECT username, text, image, likes FROM posts ORDER BY id DESC")
    posts = c.fetchall()

    conn.close()
    return posts


