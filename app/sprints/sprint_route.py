from flask import Blueprint, render_template, request, session, flash, redirect, url_for
import sqlite3
from utils import get_access, get_users, get_sprints, get_tickets

sprint_bp = Blueprint('sprint', __name__)

@sprint_bp.route('/deleteSprints', methods=['GET', 'POST'])
def deleteSprints():
    if session.get('user_id') is None:
        return render_template('index.html')
    else:
        if request.method == 'POST':
            sprint_id = request.form['Sprint']
            with sqlite3.connect("FlaskAppDB.db") as sprints:
                cursor = sprints.cursor()
                cursor.execute("DELETE FROM sprints WHERE sprintID = ?", (sprint_id,))
                cursor.execute("DELETE FROM tickets WHERE sprintID = ?", (sprint_id,))
            flash("Sprint deleted successfully!", "success")
            return redirect(url_for('page.sprints'))  
        else:
            return render_template('deleteSprints.html', sprints=get_sprints())

@sprint_bp.route('/createSprints',  methods=['GET', 'POST'])
def createSprints():
    if session.get('user_id') == None:
        return render_template('index.html')
    else:
        if request.method == 'POST':
            with sqlite3.connect("FlaskAppDB.db") as sprints:
                cursor = sprints.cursor()
                start = request.form['start']
                end = request.form['end']
                # TODO print today, compare today to start, if start < end:, cannot create sprint in the past
                if start >= end:
                    flash("Start date must be before end date.", "error")
                    return redirect(url_for('page.sprints'))
                cursor.execute("INSERT INTO sprints (sprintStart,sprintEnd) VALUES (?,?)", (start, end))
            flash("New sprint created successfully!", "success")
            return redirect(url_for('page.sprints'))
        else:
            return render_template('createSprints.html')