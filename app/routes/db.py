import sqlite3
# connect to existing db, or create
con = sqlite3.connect("FlaskAppDB.db")
# cursor can action commands on db
cur = con.cursor()
# enforce foreign key usage as not enabled by default
cur.execute("PRAGMA foreign_keys = ON;")

# Table 1: Users
cur.execute("""
CREATE TABLE IF NOT EXISTS users (
    userID INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    email TEXT NOT NULL
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
# CREATE BASE (ROOT) USER AND PASSWORD
#cur.execute("INSERT INTO users (name, email) VALUES ('root', 'root@sprints.com')")
cur.execute("INSERT INTO users (name, email) VALUES (?, ?)", ("root", "root@sprints.com"))
cur.execute("INSERT INTO logins (userID, password) VALUES (?, ?)", (1, "test"))

# QUERIES


for row in cur.execute("SELECT name FROM users"):
    print(row)

def login():
    con1 = sqlite3.connect("FlaskAppDB.db")
    cur1 = con1.cursor()
    cur1.execute("PRAGMA foreign_keys = ON;")
    username = input("Username: ")
    password = input("Password: ")
    ####################################################
    ## ADD ERROR HADNLING HERE FOR INCORRECT/NULL VALUES
    id = cur.execute("SELECT userID FROM users WHERE name=?", (username,)).fetchone()[0]
    pw = cur.execute("SELECT logins.password FROM users, logins WHERE users.userID=logins.userID & users.userID="+str(id)).fetchone()[0]
    ####################################################
    if password == str(pw):
        print("login successful")
        return id
    else:
        print("Username or Password incorrect")
        return 0
    
currentAcc = 0
while currentAcc==0:
    currentAcc = login()
    