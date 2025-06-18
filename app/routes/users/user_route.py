from flask import Blueprint, render_template, request, session, flash, redirect, url_for
import sqlite3
from app.utils.utils import get_access, get_users

user_bp = Blueprint('user', __name__)

@user_bp.route('/deleteUsers',  methods=['GET', 'POST'])
def deleteUsers():
    if session.get('user_id') == None:
        return render_template('index.html')
    else:
        if request.method == 'POST':
            with sqlite3.connect("FlaskAppDB.db") as sprints:
                cursor = sprints.cursor()
                username = request.form['User']
                userID = cursor.execute("SELECT userID FROM users WHERE name=?", (username,)).fetchone()[0]
                if session.get('user_id') == userID:
                    flash("You cannot delete your own account.", "error")
                    return redirect(url_for('page.users'))
                else:
                    cursor.execute("DELETE FROM users WHERE userID=?", (userID,))
            flash("Ticket deleted successfully!", "success")
            return redirect(url_for('page.users'))
        else:
            return render_template('deleteUsers.html', users=get_users())
               
@user_bp.route('/createUsers',  methods=['GET', 'POST'])
def createUsers():
    if session.get('user_id') == None:
        return render_template('index.html')
    else:
        if request.method == 'POST':
            with sqlite3.connect("FlaskAppDB.db") as users:
                cursor = users.cursor()
                name = request.form['name']
                if request.form.get('admin') == 'on':
                    admin = 1
                else:
                    admin = 2
                password = request.form['password']
                if cursor.execute("SELECT userID FROM users WHERE name=?", (name,)).fetchone() is not None:
                    flash("Username already exists. Please choose a different username.", "error")
                    return redirect(url_for('users'))
                cursor.execute("INSERT INTO users (name,accessID) VALUES (?,?)", (name, admin))
                cursor.execute("INSERT INTO logins (userID,password) VALUES (?,?)", (cursor.execute("SELECT userID FROM users WHERE name=?", (name,)).fetchone()[0], password))
            flash("New User created successfully!", "success")
            return redirect(url_for('page.users'))
        else:
            return render_template('createUsers.html')

@user_bp.route('/resetPass', methods=['GET', 'POST'])
def resetPass():
    if session.get('user_id') == None:
        return render_template('index.html')
    else:
        if request.method == 'POST':
            with sqlite3.connect("FlaskAppDB.db") as users:
                cursor = users.cursor()
                userID = session.get('user_id')
                password = request.form['password']
                newPass = request.form['newPass']
                existingPass = cursor.execute("SELECT password FROM logins WHERE userID=?", (userID,)).fetchone()
                if password != existingPass[0]:
                    flash("Incorrect password entered.", "error")
                    return redirect(url_for('page.home'))
                elif len(newPass) < 8 or not any(char.isdigit() for char in newPass) or not any(char.isupper() for char in newPass) or not any(char in "!@#$%^&*()-_=+[]{}|;:,.<>?/" for char in newPass):
                    flash("Password must be at least 8 characters long and contain at least 1 number, special character and capital letter.", "error")
                    return redirect(url_for('page.home'))
                else:
                    # TODO hash the password before storing it
                    cursor.execute("UPDATE logins SET password=? WHERE userID=?", (newPass, userID))
            flash("Password reset successfully!", "success")
            return redirect(url_for('page.home'))
        else:
            return render_template('resetPass.html')