#from flask import Flask, render_template, request, session
from flask import Flask, render_template, request, session, flash
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
    flash("You have been logged out.", "info")
    return render_template('index.html')

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
            return render_template('index.html')
        else:
            pw = pw[0]
        if password == str(pw):
            # create user session
            session['user_id'] = id
            session['username'] = name
            flash("Logged in successfully!", "success")
            return render_template("home.html")
        else:
            return render_template('index.html')
    else:
        return render_template('login.html')
        
@app.route('/join', methods=['GET', 'POST'])
def join():
    if request.method == 'POST':
        with sqlite3.connect("FlaskAppDB.db") as users:
            cursor = users.cursor()
            name = request.form['name']
            # TODO: check if name already exists
            password = request.form['password']
            # TODO: check if password is strong enough
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
                #TODO: check if start date is before end date
                cursor.execute("INSERT INTO sprints (sprintStart,sprintEnd) VALUES (?,?)", (start, end))
            return render_template("home.html")
        else:
            return render_template('createSprints.html')

if __name__ == '__main__':
    app.run(debug=False)