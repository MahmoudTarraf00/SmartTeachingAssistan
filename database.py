import sqlite3

DB_FILE = "app.db"


def connect():
    return sqlite3.connect(DB_FILE)


def init_db():
    db = connect()
    db.execute("CREATE TABLE IF NOT EXISTS user(name TEXT, lastname TEXT, id INT, email TEXT, password TEXT)")
    db.execute("CREATE TABLE IF NOT EXISTS sessions(session_id TEXT, user_id INT)")
    db.commit()
    db.close()



def exists(column, value):
    db = connect()
    row = db.execute(f"SELECT 1 FROM user WHERE {column} = ?", (value,)).fetchone()
    db.close()
    return row is not None


def name_exists(name, lastname):
    db = connect()
    row = db.execute("SELECT 1 FROM user WHERE name = ? AND lastname = ?", (name, lastname)).fetchone()
    db.close()
    return row is not None


def create_user(name, lastname, user_id, email, password):
    db = connect()
    db.execute("INSERT INTO user VALUES (?, ?, ?, ?, ?)", (name, lastname, user_id, email, password))
    db.commit()
    db.close()


def check_login(email, password):
    db = connect()
    user = db.execute(
        "SELECT id, name, lastname, email FROM user WHERE email = ? AND password = ?", (email, password)
    ).fetchone()
    db.close()
    return user


# sessions
def create_session(session_id, user_id):
    db = connect()
    db.execute("INSERT INTO sessions VALUES (?, ?)", (session_id, user_id))
    db.commit()
    db.close()


def get_user_by_session(session_id):
    db = connect()
    user = db.execute(
        "SELECT user.name, user.lastname, user.id, user.email "
        "FROM sessions JOIN user ON sessions.user_id = user.id "
        "WHERE sessions.session_id = ?",
        (session_id,),
    ).fetchone()
    db.close()
    return user


def delete_session(session_id):
    db = connect()
    db.execute("DELETE FROM sessions WHERE session_id = ?", (session_id,))
    db.commit()
    db.close()
