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
        descr TEXT NOT NULL,
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

    # CREATE SPRINTS
    if cur.execute("SELECT COUNT(*) FROM sprints").fetchone()[0] == 0:
        # Only insert if no sprints exist to avoid duplicates
        cur.execute("INSERT OR IGNORE INTO sprints (sprintStart, sprintEnd) VALUES (?, ?)", ("2024-01-01", "2024-01-15"))
        cur.execute("INSERT OR IGNORE INTO sprints (sprintStart, sprintEnd) VALUES (?, ?)", ("2024-01-16", "2024-01-30"))

    # CREATE TICKETS
    if cur.execute("SELECT COUNT(*) FROM tickets").fetchone()[0] == 0:
        # Only insert if no tickets exist to avoid duplicates
        cur.execute("INSERT OR IGNORE INTO tickets (sprintID, userID, descr, storyPoints) VALUES (?, ?, ?, ?)", (1, 1, "Ticket 1 Description", 5))
        cur.execute("INSERT OR IGNORE INTO tickets (sprintID, userID, descr, storyPoints) VALUES (?, ?, ?, ?)", (2, 2, "Ticket 2 Description", 3))

    cur.close()
    con.commit()
    con.close()

    