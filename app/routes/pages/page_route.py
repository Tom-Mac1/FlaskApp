from flask import Blueprint, render_template, request, session, flash, redirect, url_for
import sqlite3
from app.utils.utils import get_access, get_users, get_sprints, get_tickets
import datetime as dt 

page_bp = Blueprint('page', __name__)

@page_bp.route('/')
def index():
    return render_template('index.html')

@page_bp.route('/home')
def home():
    if session.get('user_id') == None:
        return render_template('index.html')
    return render_template('home.html')

@page_bp.route('/sprints')
def sprints():
    if session.get('user_id') == None:
        return render_template('index.html')
    else:
        sprint_id = request.args.get('sprint_id')
        connect = sqlite3.connect('FlaskAppDB.db')
        cursor = connect.cursor()
        cursor.execute('SELECT * FROM sprints')
        sprint_list = cursor.fetchall()

        if sprint_id:
            cursor.execute('SELECT * FROM sprints WHERE sprintID = ?', (sprint_id,))
            sprint = cursor.fetchone()
            cursor.execute('SELECT * FROM tickets WHERE state = ? OR sprintID = ?', ("To Do", sprint_id,))
            ticket_list = cursor.fetchall()
            selected_sprint_id = int(sprint_id)
        else:
            today = dt.datetime.today().date()
            cursor.execute('SELECT * FROM sprints WHERE sprintStart <= ? AND sprintEnd >= ?', (today, today))
            sprint = cursor.fetchone()
            if not sprint:
                sprint = sprint_list[0]
            cursor.execute('SELECT * FROM tickets WHERE state = ? OR sprintID = ?', ("To Do", sprint[0],))
            ticket_list = cursor.fetchall()
            selected_sprint_id = sprint[0]

        return render_template(
            "sprints.html",
            sprint_count=sprint_list,
            sprint_data=[sprint],
            ticket_data=ticket_list,
            selected_sprint_id=selected_sprint_id,
            access=get_access()
        )
    
@page_bp.route('/users')
def users():
    if session.get('user_id') == None:
        return render_template('index.html')
    else:
        connect = sqlite3.connect('FlaskAppDB.db')
        cursor = connect.cursor()
        cursor.execute('SELECT * FROM users')

        data = cursor.fetchall()
        return render_template("users.html", data=data, access=get_access())
    
@page_bp.route('/tickets')
def tickets():
    if session.get('user_id') == None:
        return render_template('index.html')
    else:
        print(get_access())
        connect = sqlite3.connect('FlaskAppDB.db')
        cursor = connect.cursor()
        cursor.execute('SELECT * FROM tickets')

        data = cursor.fetchall()
        return render_template("tickets.html", data=data, access=get_access())