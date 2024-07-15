import sqlite3
conn = sqlite3.connect("database.db")
cur = conn.cursor()

def create_tables():
    conn = sqlite3.connect("database.db")
    cur = conn.cursor()
    cur.execute("""CREATE TABLE IF NOT EXISTS users(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    chat_id INTEGER UNIQUE,
    user_name VARCHAR NOT NULL,
    phone_number VARCHAR NOT NULL,
    language VARCHAR NOT NULL)""")

def add_user(data: dict):
    conn = sqlite3.connect("database.db")
    cur = conn.cursor()
    cur.execute("INSERT INTO users(chat_id, user_name, phone_number, language) VALUES(?,?,?,?)",
                (data['chat_id'], data['name'], data['phone_number'], data['language']))
    conn.commit()

def check_user(chat_id):
    conn = sqlite3.connect("database.db")
    cur = conn.cursor()
    try:
        user = cur.execute("SELECT * FROM users WHERE chat_id=?", (chat_id,)).fetchone()
        return user
    except Exception as ex:
        print(ex)
        return False

def update_language(chat_id, language):
    conn = sqlite3.connect("database.db")
    cur = conn.cursor()
    cur.execute("UPDATE users SET language=? WHERE chat_id=?", (language, chat_id))
    conn.commit()