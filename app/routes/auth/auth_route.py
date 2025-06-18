from flask import Blueprint, render_template, request, session, flash, redirect, url_for
import sqlite3
from app.utils.utils import get_access, get_users, get_sprints, get_tickets

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/logout')
def logout():
    session.clear()
    flash("Successfully logged out.", "info")
    return redirect(url_for('page.index'))

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        name = request.form['name']
        id = 0
        password = request.form['password']
        con1 = sqlite3.connect("FlaskAppDB.db")
        cur1 = con1.cursor()
        cur1.execute("PRAGMA foreign_keys = ON;")
        idList = cur1.execute("SELECT userID FROM users WHERE name=?", (name,)).fetchone()
        if idList != None:
            id = idList[0]
        pw = cur1.execute("SELECT password FROM logins WHERE userID="+str(id)).fetchone()
        if pw == None:
            flash("Invalid username/password", "info")
            return redirect(url_for('auth.login'))
        else:
            pw = pw[0]
        if password == str(pw):
            # create user session
            session['user_id'] = id
            session['username'] = name
            return render_template("home.html")
        else:
            flash("Invalid username/password", "info")
            return redirect(url_for('auth.login'))
    else:
        return render_template('login.html')
        
@auth_bp.route('/join', methods=['GET', 'POST'])
def join():
    if request.method == 'POST':
        with sqlite3.connect("FlaskAppDB.db") as users:
            cursor = users.cursor()
            name = request.form['name']

            existing_user = cursor.execute("SELECT userID FROM users WHERE name=?", (name,)).fetchone()
            if existing_user is not None:
                flash("Username already exists. Please choose a different username.", "error")
                return redirect(url_for('page.index'))

            password = request.form['password']
            if len(password) < 8 or not any(char.isdigit() for char in password) or not any(char.isupper() for char in password) or not any(char in "!@#$%^&*()-_=+[]{}|;:,.<>?/" for char in password):
                flash("Password must be at least 8 characters long and contain at least 1 number, special character and capital letter.", "error")
                return redirect(url_for('page.index'))

            cursor.execute("INSERT INTO users \
            (name,accessID) VALUES (?,?)",
                            (name, 2))
            userID = cursor.execute("SELECT userID FROM users WHERE name=?", (name,)).fetchone()[0]
            # TODO hash the password before storing it
            cursor.execute("INSERT INTO logins \
            (userID,password) VALUES (?,?)",
                            (userID, password))
            idList = cursor.execute("SELECT userID FROM users WHERE name=?", (name,)).fetchone()
            id = idList[0]
            session['user_id'] = id
            session['username'] = name
        return render_template("home.html")
    else:
        return render_template('join.html')