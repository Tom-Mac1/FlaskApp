from flask import Flask, render_template, request, session, flash, redirect, url_for
import secrets
import sqlite3
from db_init import createTables, initialValues
import datetime as dt

app = Flask(__name__)
app.secret_key = secrets.token_hex(16)

createTables()
initialValues()

# Login/Session maagement ####################################
@app.route('/logout')
def logout():
    session.clear()
    flash("Successfully logged out.", "info")
    return redirect(url_for('index'))

@app.route('/login', methods=['GET', 'POST'])
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
            return redirect(url_for('login'))
        else:
            pw = pw[0]
        if password == str(pw):
            # create user session
            session['user_id'] = id
            session['username'] = name
            return render_template("home.html")
        else:
            flash("Invalid username/password", "info")
            return redirect(url_for('login'))
    else:
        return render_template('login.html')
        
@app.route('/join', methods=['GET', 'POST'])
def join():
    if request.method == 'POST':
        with sqlite3.connect("FlaskAppDB.db") as users:
            cursor = users.cursor()
            name = request.form['name']

            existing_user = cursor.execute("SELECT userID FROM users WHERE name=?", (name,)).fetchone()
            if existing_user is not None:
                flash("Username already exists. Please choose a different username.", "error")
                return redirect(url_for('index'))

            password = request.form['password']
            if len(password) < 8 or not any(char.isdigit() for char in password) or not any(char.isupper() for char in password) or not any(char in "!@#$%^&*()-_=+[]{}|;:,.<>?/" for char in password):
                flash("Password must be at least 8 characters long and contain at least 1 number, special character and capital letter.", "error")
                return redirect(url_for('index'))

            cursor.execute("INSERT INTO users \
            (name,accessID) VALUES (?,?)",
                            (name, 2))
            userID = cursor.execute("SELECT userID FROM users WHERE name=?", (name,)).fetchone()[0]
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
##############################################################

# Pages ######################################################
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/home')
def home():
    if session['user_id'] == None:
        return render_template('index.html')
    return render_template('home.html')

@app.route('/sprints')
def sprints():
    if session['user_id'] == None:
        return render_template('index.html')
    else:
        connect = sqlite3.connect('FlaskAppDB.db')
        cursor = connect.cursor()
        cursor.execute('SELECT * FROM sprints')

        data = cursor.fetchall()
        return render_template("sprints.html", data=data, access=get_access())
    
@app.route('/users')
def users():
    if session['user_id'] == None:
        return render_template('index.html')
    else:
        connect = sqlite3.connect('FlaskAppDB.db')
        cursor = connect.cursor()
        cursor.execute('SELECT * FROM users')

        data = cursor.fetchall()
        return render_template("users.html", data=data, access=get_access())
    
@app.route('/tickets')
def tickets():
    if session['user_id'] == None:
        return render_template('index.html')
    else:
        print(get_access())
        connect = sqlite3.connect('FlaskAppDB.db')
        cursor = connect.cursor()
        cursor.execute('SELECT * FROM tickets')

        data = cursor.fetchall()
        return render_template("tickets.html", data=data, access=get_access())
##############################################################

# Sprint actions #############################################  
@app.route('/deleteSprints', methods=['GET', 'POST'])
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
            return redirect(url_for('sprints'))  
        else:
            return render_template('deleteSprints.html', sprints=get_sprints())

@app.route('/createSprints',  methods=['GET', 'POST'])
def createSprints():
    if session['user_id'] == None:
        return render_template('index.html')
    else:
        if request.method == 'POST':
            with sqlite3.connect("FlaskAppDB.db") as sprints:
                cursor = sprints.cursor()
                start = request.form['start']
                end = request.form['end']
                if start >= end:
                    flash("Start date must be before end date.", "error")
                    return redirect(url_for('sprints'))
                cursor.execute("INSERT INTO sprints (sprintStart,sprintEnd) VALUES (?,?)", (start, end))
            flash("New sprint created successfully!", "success")
            return redirect(url_for('sprints'))
        else:
            return render_template('createSprints.html')
##############################################################

# TICKET ACTIONS #############################################
@app.route('/deleteTickets',  methods=['GET', 'POST'])
def deleteTickets():
    if session['user_id'] == None:
        return render_template('index.html')
    else:
        if request.method == 'POST':
            with sqlite3.connect("FlaskAppDB.db") as sprints:
                cursor = sprints.cursor()
                ticketID = request.form['Ticket']
                cursor.execute("DELETE FROM tickets WHERE ticketID=?", (ticketID,))
            flash("Ticket deleted successfully!", "success")
            return redirect(url_for('tickets'))
        else:
            return render_template('deleteTickets.html', tickets=get_tickets())

@app.route('/createTickets',  methods=['GET', 'POST'])
def createTickets():
    if session['user_id'] == None:
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
            return redirect(url_for('tickets'))
        else:
            #users and sprints for dropdown menus
            users = get_users()
            sprints = get_sprints()
            return render_template('createTickets.html', users=users, sprints=sprints)
##############################################################

# USER ACTIONS ###############################################        
@app.route('/deleteUsers',  methods=['GET', 'POST'])
def deleteUsers():
    if session['user_id'] == None:
        return render_template('index.html')
    else:
        if request.method == 'POST':
            with sqlite3.connect("FlaskAppDB.db") as sprints:
                cursor = sprints.cursor()
                username = request.form['User']
                userID = cursor.execute("SELECT userID FROM users WHERE name=?", (username,)).fetchone()[0]
                if session['user_id'] == userID:
                    flash("You cannot delete your own account.", "error")
                    return redirect(url_for('users'))
                else:
                    cursor.execute("DELETE FROM users WHERE userID=?", (userID,))
            flash("Ticket deleted successfully!", "success")
            return redirect(url_for('users'))
        else:
            return render_template('deleteUsers.html', users=get_users())
               
@app.route('/createUsers',  methods=['GET', 'POST'])
def createUsers():
    if session['user_id'] == None:
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
            return redirect(url_for('users'))
        else:
            return render_template('createUsers.html')

@app.route('/resetPass', methods=['GET', 'POST'])
def resetPass():
    if session['user_id'] == None:
        return render_template('index.html')
    else:
        if request.method == 'POST':
            with sqlite3.connect("FlaskAppDB.db") as users:
                cursor = users.cursor()
                userID = session['user_id']
                password = request.form['password']
                newPass = request.form['newPass']
                existingPass = cursor.execute("SELECT password FROM logins WHERE userID=?", (userID,)).fetchone()
                if password != existingPass[0]:
                    flash("Incorrect password entered.", "error")
                    return redirect(url_for('resetPass'))
                elif len(newPass) < 8 or not any(char.isdigit() for char in newPass) or not any(char.isupper() for char in newPass) or not any(char in "!@#$%^&*()-_=+[]{}|;:,.<>?/" for char in newPass):
                    flash("Password must be at least 8 characters long and contain at least 1 number, special character and capital letter.", "error")
                    return redirect(url_for('home'))
                else:
                    cursor.execute("UPDATE logins SET password=? WHERE userID=?", (newPass, userID))
            flash("Password reset successfully!", "success")
            return redirect(url_for('home'))
        else:
            return render_template('resetPass.html')
##############################################################

# Getter functions ###########################################
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
##############################################################

if __name__ == '__main__':
    app.run(debug=False)