from flask import Blueprint, render_template, request, session, flash, redirect, url_for
import sqlite3
from app.utils.utils import get_users, get_future_sprints, get_ticket_by_id

ticket_bp = Blueprint('ticket', __name__)

@ticket_bp.route('/deleteTicket/<int:ticket_id>',  methods=['GET', 'POST'])
def deleteTickets(ticket_id):
    if session.get('user_id') == None:
        return render_template('index.html')
    else:
        with sqlite3.connect("FlaskAppDB.db") as sprints:
            cursor = sprints.cursor()
            cursor.execute("DELETE FROM tickets WHERE ticketID=?", (ticket_id,))
        flash("Ticket deleted successfully!", "success")
        return redirect(url_for('page.tickets'))

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
            users = get_users()
            sprints = get_future_sprints()
            return render_template('createTickets.html', users=users, sprints=sprints)

@ticket_bp.route('/editTickets<int:ticket_id>',  methods=['GET', 'POST'])
def editTickets(ticket_id):
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
                cursor.execute("UPDATE tickets SET descr=?, userID=?, storyPoints=?, sprintID=? WHERE ticketID=?", (description, id, points, sprint, ticket_id))
            flash("Ticket updated successfully!", "success")
            return redirect(url_for('page.tickets'))
        else:
            return render_template('editTickets.html', sprints=get_future_sprints(), users=get_users(), ticket=get_ticket_by_id(ticket_id))
