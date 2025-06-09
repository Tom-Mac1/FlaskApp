#from flask import Flask, render_template, request, session
from flask import Flask, render_template, request, session, flash, redirect, url_for
import secrets
import sqlite3
from db_init import createTables, initialValues

app = Flask(__name__)
app.secret_key = secrets.token_hex(16)

createTables()
initialValues()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/logout')
def logout():
    session.clear()
    flash("Successfully logged out.", "info")
    return redirect(url_for('index'))
    #return render_template('index.html')

@app.route('/home')
def home():
    if session['user_id'] == None:
        return render_template('index.html')
    return render_template('home.html')

@app.route('/about')
def about():
    return render_template('about.html')

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
            # new #
            existing_user = cursor.execute("SELECT userID FROM users WHERE name=?", (name,)).fetchone()
            if existing_user is not None:
                flash("Username already exists. Please choose a different username.", "error")
                return redirect(url_for('join'))
            #     #
            password = request.form['password']
            # new #
            # if <8 char, no num, no capital ltr or special char, return error
            if len(password) < 8 or not any(char.isdigit() for char in password) or not any(char.isupper() for char in password) or not any(char in "!@#$%^&*()-_=+[]{}|;:,.<>?/" for char in password):
                flash("Password must be at least 8 characters long and contain at least 1 number, special character and capital letter.", "error")
                return redirect(url_for('join'))
            #     #
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

@app.route('/sprints')
def sprints():
    if session['user_id'] == None:
        return render_template('index.html')
    else:
        connect = sqlite3.connect('FlaskAppDB.db')
        cursor = connect.cursor()
        cursor.execute('SELECT * FROM sprints')

        data = cursor.fetchall()
        return render_template("sprints.html", data=data)
    
@app.route('/users')
def users():
    if session['user_id'] == None:
        return render_template('index.html')
    else:
        connect = sqlite3.connect('FlaskAppDB.db')
        cursor = connect.cursor()
        cursor.execute('SELECT * FROM users')

        data = cursor.fetchall()
        return render_template("users.html", data=data)
    
@app.route('/tickets')
def tickets():
    if session['user_id'] == None:
        return render_template('index.html')
    else:
        connect = sqlite3.connect('FlaskAppDB.db')
        cursor = connect.cursor()
        cursor.execute('SELECT * FROM tickets')

        data = cursor.fetchall()
        return render_template("tickets.html", data=data)

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
                # new #
                if start >= end:
                    flash("Start date must be before end date.", "error")
                    return redirect(url_for('createSprints'))
                #     #
                cursor.execute("INSERT INTO sprints (sprintStart,sprintEnd) VALUES (?,?)", (start, end))
            flash("New sprint created successfully!", "success")
            return redirect(url_for('sprints'))
        else:
            return render_template('createSprints.html')

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
                cursor.execute("INSERT INTO tickets (descr,userID) VALUES (?,?)", (description, id))
            flash("New ticket created successfully!", "success")
            return redirect(url_for('tickets'))
        else:
            users = get_users()
            # new #
            sprints = get_sprints()
            #     #
            return render_template('createTickets.html', users=users, sprints=sprints)

def get_users():
    conn = sqlite3.connect('FlaskAppDB.db')
    cur = conn.cursor()
    cur.execute("SELECT name FROM users")
    users = cur.fetchall()
    conn.close()
    return [user[0] for user in users]

# new #
def get_sprints():
    date = "01-01-2023"
    conn = sqlite3.connect('FlaskAppDB.db')
    cur = conn.cursor()
    cur.execute("SELECT sprintID FROM sprints WHERE sprintStart >= ?", (date,))
    sprints = cur.fetchall()
    conn.close()
    return [sprint[0] for sprint in sprints]
#    #

if __name__ == '__main__':
    app.run(debug=False)