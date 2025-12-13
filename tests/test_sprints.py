import sqlite3
import datetime as dt

# Should not be able to create sprint without logging in
def test_create_sprint_not_logged_in(client):
    resp = client.post("/createSprints")
    assert resp.status_code == 200
    assert b"Log in or sign up" in resp.data

# Should be able to create sprint without error
def test_create_sprint_success(admin_client):
    today = dt.date.today()
    start = today + dt.timedelta(days=1)
    end = today + dt.timedelta(days=7)

    resp = admin_client.post(
        "/createSprints",
        data={
            "start": start.strftime("%Y-%m-%d"),
            "end": end.strftime("%Y-%m-%d"),
        },
        follow_redirects=True,
    )
    assert resp.status_code == 200

# Should not be able to delete sprint without logging in
def test_delete_sprint_unauthorized(user_client):
    resp = user_client.get("/deleteSprints1", follow_redirects=True)
    assert b"Log in or sign up" in resp.data or b"Unauthorized" in resp.data

# Should be able to delete sprint without error
def test_delete_sprint_admin(admin_client):
    conn = sqlite3.connect("FlaskAppDB.db")
    cur = conn.cursor()
    cur.execute(
        "INSERT INTO sprints (sprintStart, sprintEnd) VALUES (?, ?)",
        ("2035-01-01", "2035-01-10"),
    )
    sprint_id = cur.lastrowid
    conn.commit()
    conn.close()

    resp = admin_client.get(f"/deleteSprints{sprint_id}", follow_redirects=True)

    assert resp.status_code == 200
    assert b"Sprint deleted successfully" in resp.data
