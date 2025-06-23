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


    # CREATE 9 STANDARD USERS AND PASSWORDS
    cur.execute("INSERT OR IGNORE INTO users (name, accessID) VALUES (?, ?)", ("User1", 2))
    cur.execute("INSERT OR IGNORE INTO logins (userID, password) VALUES (?, ?)", (2, "User1PW"))
    cur.execute("INSERT OR IGNORE INTO users (name, accessID) VALUES (?, ?)", ("User2", 2))
    cur.execute("INSERT OR IGNORE INTO logins (userID, password) VALUES (?, ?)", (3, "User2PW"))
    cur.execute("INSERT OR IGNORE INTO users (name, accessID) VALUES (?, ?)", ("User3", 2))
    cur.execute("INSERT OR IGNORE INTO logins (userID, password) VALUES (?, ?)", (4, "User3PW"))
    cur.execute("INSERT OR IGNORE INTO users (name, accessID) VALUES (?, ?)", ("User4", 2))
    cur.execute("INSERT OR IGNORE INTO logins (userID, password) VALUES (?, ?)", (5, "User4PW"))
    cur.execute("INSERT OR IGNORE INTO users (name, accessID) VALUES (?, ?)", ("User5", 2))
    cur.execute("INSERT OR IGNORE INTO logins (userID, password) VALUES (?, ?)", (6, "User5PW"))
    cur.execute("INSERT OR IGNORE INTO users (name, accessID) VALUES (?, ?)", ("User6", 2))
    cur.execute("INSERT OR IGNORE INTO logins (userID, password) VALUES (?, ?)", (7, "User6PW"))
    cur.execute("INSERT OR IGNORE INTO users (name, accessID) VALUES (?, ?)", ("User7", 2))
    cur.execute("INSERT OR IGNORE INTO logins (userID, password) VALUES (?, ?)", (8, "User7PW"))
    cur.execute("INSERT OR IGNORE INTO users (name, accessID) VALUES (?, ?)", ("User8", 2))
    cur.execute("INSERT OR IGNORE INTO logins (userID, password) VALUES (?, ?)", (9, "User8PW"))
    cur.execute("INSERT OR IGNORE INTO users (name, accessID) VALUES (?, ?)", ("User9", 2))
    cur.execute("INSERT OR IGNORE INTO logins (userID, password) VALUES (?, ?)", (10, "User9PW"))

    # CREATE SPRINTS
    if cur.execute("SELECT COUNT(*) FROM sprints").fetchone()[0] == 0:
        # Only insert if no sprints exist to avoid duplicates
        # 10 default sprints, 2 for each month of the year
        cur.execute("INSERT OR IGNORE INTO sprints (sprintStart, sprintEnd) VALUES (?, ?)", ("2024-01-01", "2024-01-15"))
        cur.execute("INSERT OR IGNORE INTO sprints (sprintStart, sprintEnd) VALUES (?, ?)", ("2024-01-16", "2024-01-30"))
        cur.execute("INSERT OR IGNORE INTO sprints (sprintStart, sprintEnd) VALUES (?, ?)", ("2024-02-01", "2024-02-15"))
        cur.execute("INSERT OR IGNORE INTO sprints (sprintStart, sprintEnd) VALUES (?, ?)", ("2024-02-16", "2024-02-29"))
        cur.execute("INSERT OR IGNORE INTO sprints (sprintStart, sprintEnd) VALUES (?, ?)", ("2024-03-01", "2024-03-15"))
        cur.execute("INSERT OR IGNORE INTO sprints (sprintStart, sprintEnd) VALUES (?, ?)", ("2024-03-16", "2024-03-31"))
        cur.execute("INSERT OR IGNORE INTO sprints (sprintStart, sprintEnd) VALUES (?, ?)", ("2024-04-01", "2024-04-15"))
        cur.execute("INSERT OR IGNORE INTO sprints (sprintStart, sprintEnd) VALUES (?, ?)", ("2024-04-16", "2024-04-30"))
        cur.execute("INSERT OR IGNORE INTO sprints (sprintStart, sprintEnd) VALUES (?, ?)", ("2024-05-01", "2024-05-15"))
        cur.execute("INSERT OR IGNORE INTO sprints (sprintStart, sprintEnd) VALUES (?, ?)", ("2024-05-16", "2024-05-31"))

    # CREATE TICKETS
    if cur.execute("SELECT COUNT(*) FROM tickets").fetchone()[0] == 0:
        # Only insert if no tickets exist to avoid duplicates
        sprintID = cur.execute("SELECT sprintID FROM sprints").fetchall()
        if (1 in sprintID) and (2 in sprintID):
            cur.execute("INSERT OR IGNORE INTO tickets (sprintID, userID, descr, storyPoints) VALUES (?, ?, ?, ?)", (sprintID, 1, "Ticket 1 Description", 5))
            cur.execute("INSERT OR IGNORE INTO tickets (sprintID, userID, descr, storyPoints) VALUES (?, ?, ?, ?)", (sprintID, 2, "Ticket 2 Description", 3))
            cur.execute("INSERT OR IGNORE INTO tickets (sprintID, userID, descr, storyPoints) VALUES (?, ?, ?, ?)", (sprintID, 1, "Ticket 3 Description", 8))
            cur.execute("INSERT OR IGNORE INTO tickets (sprintID, userID, descr, storyPoints) VALUES (?, ?, ?, ?)", (sprintID, 2, "Ticket 4 Description", 2))
            cur.execute("INSERT OR IGNORE INTO tickets (sprintID, userID, descr, storyPoints) VALUES (?, ?, ?, ?)", (sprintID, 1, "Ticket 5 Description", 13))
            cur.execute("INSERT OR IGNORE INTO tickets (sprintID, userID, descr, storyPoints) VALUES (?, ?, ?, ?)", (sprintID, 2, "Ticket 6 Description", 1))
            cur.execute("INSERT OR IGNORE INTO tickets (sprintID, userID, descr, storyPoints) VALUES (?, ?, ?, ?)", (sprintID, 1, "Ticket 7 Description", 21))
            cur.execute("INSERT OR IGNORE INTO tickets (sprintID, userID, descr, storyPoints) VALUES (?, ?, ?, ?)", (sprintID, 2, "Ticket 8 Description", 3))
            cur.execute("INSERT OR IGNORE INTO tickets (sprintID, userID, descr, storyPoints) VALUES (?, ?, ?, ?)", (sprintID, 1, "Ticket 9 Description", 5))
            cur.execute("INSERT OR IGNORE INTO tickets (sprintID, userID, descr, storyPoints) VALUES (?, ?, ?, ?)", (sprintID, 2, "Ticket 10 Description", 8))

    cur.close()
    con.commit()
    con.close()

    