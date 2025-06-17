from flask import Blueprint, render_template, request, session, flash, redirect, url_for
import sqlite3
from utils import get_access, get_users, get_sprints, get_tickets

ticket_bp = Blueprint('ticket', __name__)

@ticket_bp.route('/deleteTickets',  methods=['GET', 'POST'])
def deleteTickets():
    if session.get('user_id') == None:
        return render_template('index.html')
    else:
        if request.method == 'POST':
            with sqlite3.connect("FlaskAppDB.db") as sprints:
                cursor = sprints.cursor()
                ticketID = request.form['Ticket']
                cursor.execute("DELETE FROM tickets WHERE ticketID=?", (ticketID,))
            flash("Ticket deleted successfully!", "success")
            return redirect(url_for('page.tickets'))
        else:
            return render_template('deleteTickets.html', tickets=get_tickets())

@ticket_bp.route('/createTickets',  methods=['GET', 'POST'])
def createTickets():
    if session.get('user_id') == None:
        return render_template('index.html')
    else:
        if request.method == 'POST':
            with sqlite3.connect("FlaskAppDB.db") as sprints:
                cursor = sprints.cursor()
                description = request.form['Description']
                assigned = request.form['Assigned']
                idList = cursor.execute("SELECT userID FROM users WHERE name=?", (assigned,)).fetchone()
                id = idList[0]
                points = int(request.form['StoryPoints'])
                sprint = int(request.form['Sprint'])
                cursor.execute("INSERT INTO tickets (descr,userID,storyPoints,sprintID) VALUES (?,?,?,?)", (description, id, points, sprint))
            flash("New ticket created successfully!", "success")
            return redirect(url_for('page.tickets'))
        else:
            #users and sprints for dropdown menus
            users = get_users()
            sprints = get_sprints()
            return render_template('createTickets.html', users=users, sprints=sprints)
