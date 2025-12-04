from flask import Blueprint, render_template, request, session, flash, redirect, url_for, jsonify
import sqlite3
from app.utils.utils import get_users, get_future_sprints, get_ticket_by_id

ticket_bp = Blueprint('ticket', __name__)


@ticket_bp.route('/deleteTicket/<int:ticket_id>',  methods=['GET', 'POST'])
def deleteTickets(ticket_id):
    if session.get('user_id') is None:
        return render_template('index.html')
    else:
        with sqlite3.connect("FlaskAppDB.db") as sprints:
            cursor = sprints.cursor()
            cursor.execute("DELETE FROM tickets WHERE ticketID=?", (ticket_id,))
        flash("Ticket deleted successfully!", "success")
        return redirect(url_for('page.sprints'))


@ticket_bp.route('/createTickets',  methods=['GET', 'POST'])
def createTickets():
    if session.get('user_id') is None:
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
                cursor.execute("INSERT INTO tickets (descr,userID,storyPoints) VALUES (?,?,?)", (description, id, points))
            flash("New ticket created successfully!", "success")
            return redirect(url_for('page.sprints'))
        else:
            users = get_users()
            sprints = get_future_sprints()
            return render_template('createTickets.html', users=users, sprints=sprints)


@ticket_bp.route('/editTickets<int:ticket_id>',  methods=['GET', 'POST'])
def editTickets(ticket_id):
    if session.get('user_id') is None:
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
                sprint = cursor.execute("SELECT sprintID FROM tickets WHERE ticketID=?", (ticket_id,)).fetchone()[0]
                cursor.execute("UPDATE tickets SET descr=?, userID=?, storyPoints=? WHERE ticketID=?", (description, id, points, ticket_id))
            flash("Ticket updated successfully!", "success")
            return redirect(url_for('page.sprints', sprint_id=sprint))
        else:
            return render_template('editTickets.html', sprints=get_future_sprints(), users=get_users(), ticket=get_ticket_by_id(ticket_id))


@ticket_bp.route('/update_ticket_status/<int:ticket_id>', methods=['POST'])
def update_ticket_status(ticket_id):
    data = request.get_json()
    new_state = data.get('state')
    sprint = data.get('sprint')

    if not new_state:
        print("state missing")
        return jsonify({'error': 'Missing state'}), 400
    elif not sprint:
        print("sprint missing")
        return jsonify({'error': 'Missing sprint'}), 400
    try:
        with sqlite3.connect("FlaskAppDB.db") as tickets:
            cursor = tickets.cursor()
            print(f"Updating ticket {ticket_id} to state {new_state} and sprint {sprint}")
            cursor.execute("UPDATE tickets SET state=?, sprintID=? WHERE ticketID=?", (new_state, sprint, ticket_id))
            tickets.commit()
            print("Update successful")
            return jsonify({'success': True, 'ticket_id': ticket_id, 'new_state': new_state}), 200
    except Exception as e:
        print("Error updating ticket:", e)
        return jsonify({'error': str(e)}), 500
