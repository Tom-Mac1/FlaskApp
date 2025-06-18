import sqlite3
from flask import session

def get_access():
    conn = sqlite3.connect('FlaskAppDB.db')
    cur = conn.cursor()
    cur.execute("SELECT accessID FROM users WHERE userID=?", (session['user_id'],))
    access = cur.fetchone()
    conn.close()
    return int(access[0])
    
def get_users():
    conn = sqlite3.connect('FlaskAppDB.db')
    cur = conn.cursor()
    cur.execute("SELECT name FROM users")
    users = cur.fetchall()
    conn.close()
    return [user[0] for user in users]

def get_sprints():
    conn = sqlite3.connect('FlaskAppDB.db')
    cur = conn.cursor()
    cur.execute("SELECT sprintID FROM sprints")
    sprints = cur.fetchall()
    print(sprints)
    conn.close()
    return [sprint[0] for sprint in sprints]

def get_tickets():
    conn = sqlite3.connect('FlaskAppDB.db')
    cur = conn.cursor()
    cur.execute("SELECT ticketID FROM tickets")
    tickets = cur.fetchall()
    conn.close()
    return [ticket[0] for ticket in tickets]

def get_future_sprints():
    conn = sqlite3.connect('FlaskAppDB.db')
    cur = conn.cursor()
    cur.execute("SELECT sprintID FROM sprints WHERE sprintStart > date('now')")
    sprints = cur.fetchall()
    conn.close()
    return [sprint[0] for sprint in sprints]