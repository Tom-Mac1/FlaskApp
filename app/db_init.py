import sqlite3
def createTables():
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
        name TEXT UNIQUE NOT NULL,
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
        sprintStart TEXT NOT NULL, -- DD-MM-YYYY format
        sprintEnd TEXT NOT NULL -- DD-MM-YYYY format
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
    cur.close()
    con.commit()
    con.close()
    
def initialValues():
    # connect to existing db, or create
    con = sqlite3.connect("FlaskAppDB.db")
    # cursor can action commands on db
    cur = con.cursor()
    # enforce foreign key usage as not enabled by default
    cur.execute("PRAGMA foreign_keys = ON;")
    # CREATE ADMIN (ROOT) USER AND PASSWORD
    cur.execute("INSERT OR IGNORE INTO users (name, accessID) VALUES (?, ?)", ("root", 1))
    cur.execute("INSERT OR IGNORE INTO logins (userID, password) VALUES (?, ?)", (1, "rootPW"))

    # CREATE STANDARD USER AND PASSWORD
    cur.execute("INSERT OR IGNORE INTO users (name, accessID) VALUES (?, ?)", ("User1", 2))
    cur.execute("INSERT OR IGNORE INTO logins (userID, password) VALUES (?, ?)", (2, "User1PW"))

    # CREATE TEST SPRINT
    cur.execute("INSERT OR IGNORE INTO sprints (sprintStart, sprintEnd) VALUES (?, ?)", ('2000-01-01', '2001-01-01'))
    cur.close()
    con.commit()
    con.close()

    