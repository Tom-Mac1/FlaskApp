import sqlite3

# Should be able to create ticket when logged in
def test_create_ticket(user_client):
    conn = sqlite3.connect("FlaskAppDB.db")
    cur = conn.cursor()

    cur.execute(
        "INSERT OR IGNORE INTO users (name, accessID) VALUES (?, ?)",
        ("ticketuser", 0),
    )
    conn.commit()
    conn.close()

    resp = user_client.post(
        "/createTickets",
        data={
            "Description": "Test ticket",
            "Assigned": "ticketuser",
            "StoryPoints": "5",
        },
        follow_redirects=True,
    )

    assert resp.status_code == 200
    assert b"ticket" in resp.data.lower()
