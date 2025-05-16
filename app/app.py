from flask import Flask, render_template, request
import sqlite3
from db_init import createTables, initialValues

app = Flask(__name__)

# find a way around the fact that db must be deleted every run
createTables()
initialValues()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/home')
def home():
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
            #set a message to display saying invalid password or username
            return render_template('index.html')
        else:
            pw = pw[0]
        if password == str(pw):
            return render_template("home.html")
        else:
            #set a message to display saying invalid password or username
            return render_template('index.html')
    else:
        return render_template('login.html')
        
@app.route('/join', methods=['GET', 'POST'])
def join():
    with sqlite3.connect("FlaskAppDB.db") as users:
        cursor = users.cursor()
        name = request.form['name']
        password = request.form['password']
        cursor.execute("INSERT INTO users \
        (name,accessID) VALUES (?,?)",
                        (name, 2))
        userID = cursor.execute("SELECT userID FROM users WHERE name = ?", (name,)).fetchone()[0]
        cursor.execute("INSERT INTO logins \
        (userID,password) VALUES (?,?)",
                        (userID, password))
        cursor.close()
        users.commit()
        users.close()

@app.route('/sprints')
def sprints():
    connect = sqlite3.connect('FlaskAppDB.db')
    cursor = connect.cursor()
    cursor.execute('SELECT * FROM users')

    data = cursor.fetchall()
    return render_template("sprints.html", data=data)

if __name__ == '__main__':
    app.run(debug=False)