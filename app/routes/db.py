import sqlite3
# connect to existing db, or create
con = sqlite3.connect("FlaskAppDB.db")
# cursor can action commands on db
cur = con.cursor()
# enforce foreign key usage as not enabled by default
cur.execute("PRAGMA foreign_keys = ON;")

# Table 1: Users
# AccessID: 1 = admin, 2 = user
cur.execute("""
CREATE TABLE IF NOT EXISTS users (
    userID INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    accessID INTEGER NOT NULL
)
""")

# Table 2: Logins 
cur.execute("""
CREATE TABLE IF NOT EXISTS logins (
    userID INTEGER PRIMARY KEY,
    password TEXT NOT NULL,
    FOREIGN KEY (userID) REFERENCES users(userID)
)
""")

# Table 3: Sprints
cur.execute("""
CREATE TABLE IF NOT EXISTS sprints (
    sprintID INTEGER PRIMARY KEY AUTOINCREMENT,
    sprintStart TIMESTAMP NOT NULL,
    sprintEnd TIMESTAMP NOT NULL
)
""")

# Table 4: Tickets
cur.execute("""
CREATE TABLE IF NOT EXISTS tickets (
    ticketID INTEGER PRIMARY KEY AUTOINCREMENT,
    sprintID INTEGER,
    userID INTEGER,
    desc TEXT NOT NULL,
    storyPoints INTEGER,
    FOREIGN KEY (sprintID) REFERENCES sprints(sprintID),
    FOREIGN KEY (userID) REFERENCES users(userID)
)
""")

# CREATE ADMIN (ROOT) USER AND PASSWORD
cur.execute("INSERT INTO users (name, accessID) VALUES (?, ?)", ("root", 1))
cur.execute("INSERT INTO logins (userID, password) VALUES (?, ?)", (1, "rootPW"))

# CREATE STANDARD USER AND PASSWORD
cur.execute("INSERT INTO users (name, accessID) VALUES (?, ?)", ("User1", 2))
cur.execute("INSERT INTO logins (userID, password) VALUES (?, ?)", (2, "User1PW"))

# Login
def login():
    con1 = sqlite3.connect("FlaskAppDB.db")
    cur1 = con1.cursor()
    cur1.execute("PRAGMA foreign_keys = ON;")
    username = input("Username: ")
    password = input("Password: ")
    idList = cur.execute("SELECT userID FROM users WHERE name=?", (username,)).fetchone()
    if idList != None:
        id = idList[0]
    else:
        id = 0
    pw = cur.execute("SELECT password FROM logins WHERE userID="+str(id)).fetchone()
    if pw == None:
        print("Username or Password incorrect")
        return 0
    else:
        pw = pw[0]
    if password == str(pw):
        print("login successful")
        return id
    else:
        print("Username or Password incorrect")
        return 0

# If current account is 0 then there is no active session
# Current account will link to account number of active user session
currentAcc = 0
while currentAcc==0:
    currentAcc = login()
    