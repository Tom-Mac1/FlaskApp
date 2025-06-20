from flask import Blueprint, render_template, request, session, flash, redirect, url_for
import sqlite3
from app.utils.utils import get_sprints, get_sprint_dates
import datetime as dt

sprint_bp = Blueprint('sprint', __name__)

@sprint_bp.route('/deleteSprints<int:sprint_id>', methods=['GET', 'POST'])
def deleteSprints(sprint_id):
    if session.get('user_id') is None:
        return render_template('index.html')
    else:
        with sqlite3.connect("FlaskAppDB.db") as sprints:
            cursor = sprints.cursor()
            cursor.execute("DELETE FROM sprints WHERE sprintID = ?", (sprint_id,))
            cursor.execute("DELETE FROM tickets WHERE sprintID = ?", (sprint_id,))
        flash("Sprint deleted successfully!", "success")
        return redirect(url_for('page.sprints'))
    
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
                start_date = dt.datetime.strptime(start, "%Y-%m-%d")
                end_date = dt.datetime.strptime(end, "%Y-%m-%d")
                today = dt.datetime.today().date()
                if start_date.date() < today:
                    flash("Start date cannot start in the past.", "error")
                    return redirect(url_for('page.sprints'))
                if start >= end:
                    flash("Start date must be before end date.", "error")
                    return redirect(url_for('page.sprints'))
                other_sprints = get_sprint_dates()
                for sprint in other_sprints:
                    if start_date.date() < sprint['sprintEnd'] and end_date.date() > sprint['sprintStart']:
                        flash("New sprint overlaps with an existing sprint.", "error")
                        return redirect(url_for('page.sprints'))
                cursor.execute("INSERT INTO sprints (sprintStart,sprintEnd) VALUES (?,?)", (start, end))
            flash("New sprint created successfully!", "success")
            return redirect(url_for('page.sprints'))
        else:
            return render_template('createSprints.html')