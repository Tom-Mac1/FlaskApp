import sqlite3

# Test inserting a user into the users table
def test_user_insert():
    conn = sqlite3.connect("FlaskAppDB.db")
    cur = conn.cursor()

    cur.execute(
        "INSERT OR IGNORE INTO users (name, accessID) VALUES (?, ?)",
        ("pytestuser", 0),
    )
    conn.commit()

    user = cur.execute(
        "SELECT name FROM users WHERE name=?",
        ("pytestuser",),
    ).fetchone()

    conn.close()

    assert user is not None
    assert user[0] == "pytestuser"
