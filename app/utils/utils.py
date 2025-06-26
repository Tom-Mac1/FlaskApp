import sqlite3
from flask import session
import datetime as dt

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

def get_sprint_dates():
    conn = sqlite3.connect('FlaskAppDB.db')
    cur = conn.cursor()
    cur.execute("SELECT sprintStart, sprintEnd FROM sprints")
    sprints = cur.fetchall()
    conn.close()
    print(sprints)
    return [
        {
            'sprintStart': dt.datetime.strptime(sprint[0], '%Y-%m-%d').date(),
            'sprintEnd': dt.datetime.strptime(sprint[1], '%Y-%m-%d').date()
        }
        for sprint in sprints
    ]

# This function retrieves a ticket by its ID and returns its details along with the user's name.
def get_ticket_by_id(ticket_id):
    conn = sqlite3.connect('FlaskAppDB.db')
    cur = conn.cursor()
    cur.execute("SELECT * FROM tickets WHERE ticketID=?", (ticket_id,))
    ticket = cur.fetchone()
    user = cur.execute("SELECT name FROM users WHERE userID=?", (ticket[2],)).fetchone()
    conn.close()
    if ticket:
        return {
            'ticketID': ticket[0],
            'sprintID': ticket[1],
            'user': user[0],
            'descr': ticket[3],
            'storyPoints': ticket[4]
        }
    return None