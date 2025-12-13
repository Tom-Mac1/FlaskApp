import sqlite3
import bcrypt


def test_password_is_hashed():
    conn = sqlite3.connect("FlaskAppDB.db")
    cur = conn.cursor()
    pw = cur.execute(
        "SELECT password_hashed FROM logins WHERE userID=1"
    ).fetchone()[0]

    assert not pw == "User1PW"
    assert pw.startswith("$2b$")

def test_sql_injection_login_attempt(client):
    response = client.post("/login", data={
        "name": "' OR 1=1 --",
        "password": "anything"
    }, follow_redirects=True)
    assert b"Invalid username/password" in response.data