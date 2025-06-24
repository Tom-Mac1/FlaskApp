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
    userID = cur.execute("SELECT userID FROM users WHERE name = ?", ("root",)).fetchone()[0]
    cur.execute("INSERT OR IGNORE INTO logins (userID, password) VALUES (?, ?)", (userID, "rootPW"))

    # CREATE 9 STANDARD USERS AND PASSWORDS
    userTotal = cur.execute("SELECT COUNT(*) FROM users").fetchone()[0]
    if userTotal <= 2:
        cur.execute("INSERT OR IGNORE INTO users (name, accessID) VALUES (?, ?)", ("User1", 2))
        userID = cur.execute("SELECT userID FROM users WHERE name = ?", ("User1",)).fetchone()[0]
        cur.execute("INSERT OR IGNORE INTO logins (userID, password) VALUES (?, ?)", (userID, "User1PW"))
        cur.execute("INSERT OR IGNORE INTO users (name, accessID) VALUES (?, ?)", ("User2", 2))
        userID = cur.execute("SELECT userID FROM users WHERE name = ?", ("User2",)).fetchone()[0]
        cur.execute("INSERT OR IGNORE INTO logins (userID, password) VALUES (?, ?)", (userID, "User2PW"))
        cur.execute("INSERT OR IGNORE INTO users (name, accessID) VALUES (?, ?)", ("User3", 2))
        userID = cur.execute("SELECT userID FROM users WHERE name = ?", ("User3",)).fetchone()[0]
        cur.execute("INSERT OR IGNORE INTO logins (userID, password) VALUES (?, ?)", (userID, "User3PW"))
        cur.execute("INSERT OR IGNORE INTO users (name, accessID) VALUES (?, ?)", ("User4", 2))
        userID = cur.execute("SELECT userID FROM users WHERE name = ?", ("User4",)).fetchone()[0]
        cur.execute("INSERT OR IGNORE INTO logins (userID, password) VALUES (?, ?)", (userID, "User4PW"))
        cur.execute("INSERT OR IGNORE INTO users (name, accessID) VALUES (?, ?)", ("User5", 2))
        userID = cur.execute("SELECT userID FROM users WHERE name = ?", ("User5",)).fetchone()[0]
        cur.execute("INSERT OR IGNORE INTO logins (userID, password) VALUES (?, ?)", (userID, "User5PW"))
        cur.execute("INSERT OR IGNORE INTO users (name, accessID) VALUES (?, ?)", ("User6", 2))
        userID = cur.execute("SELECT userID FROM users WHERE name = ?", ("User6",)).fetchone()[0]
        cur.execute("INSERT OR IGNORE INTO logins (userID, password) VALUES (?, ?)", (userID, "User6PW"))
        cur.execute("INSERT OR IGNORE INTO users (name, accessID) VALUES (?, ?)", ("User7", 2))
        userID = cur.execute("SELECT userID FROM users WHERE name = ?", ("User7",)).fetchone()[0]
        cur.execute("INSERT OR IGNORE INTO logins (userID, password) VALUES (?, ?)", (userID, "User7PW"))
        cur.execute("INSERT OR IGNORE INTO users (name, accessID) VALUES (?, ?)", ("User8", 2))
        userID = cur.execute("SELECT userID FROM users WHERE name = ?", ("User8",)).fetchone()[0]
        cur.execute("INSERT OR IGNORE INTO logins (userID, password) VALUES (?, ?)", (userID, "User8PW"))
        cur.execute("INSERT OR IGNORE INTO users (name, accessID) VALUES (?, ?)", ("User9", 2))
        userID = cur.execute("SELECT userID FROM users WHERE name = ?", ("User9",)).fetchone()[0]
        cur.execute("INSERT OR IGNORE INTO logins (userID, password) VALUES (?, ?)", (userID, "User9PW"))
    else:
        print("Users already exist, skipping user creation.")

    # CREATE SPRINTS
    print(cur.execute("SELECT COUNT(*) FROM sprints").fetchone())
    if cur.execute("SELECT COUNT(*) FROM sprints").fetchone()[0] == 0:
        # Only insert if no sprints exist to avoid duplicates
        # 10 default sprints, 2 for each month of the year
        cur.execute("INSERT OR IGNORE INTO sprints (sprintStart, sprintEnd) VALUES (?, ?)", ("2026-01-01", "2026-01-15"))
        cur.execute("INSERT OR IGNORE INTO sprints (sprintStart, sprintEnd) VALUES (?, ?)", ("2026-01-16", "2026-01-20"))
        cur.execute("INSERT OR IGNORE INTO sprints (sprintStart, sprintEnd) VALUES (?, ?)", ("2026-02-01", "2026-02-15"))
        cur.execute("INSERT OR IGNORE INTO sprints (sprintStart, sprintEnd) VALUES (?, ?)", ("2026-02-16", "2026-02-22"))
        cur.execute("INSERT OR IGNORE INTO sprints (sprintStart, sprintEnd) VALUES (?, ?)", ("2026-03-01", "2026-03-15"))
        cur.execute("INSERT OR IGNORE INTO sprints (sprintStart, sprintEnd) VALUES (?, ?)", ("2026-03-16", "2026-03-21"))
        cur.execute("INSERT OR IGNORE INTO sprints (sprintStart, sprintEnd) VALUES (?, ?)", ("2026-04-01", "2026-04-15"))
        cur.execute("INSERT OR IGNORE INTO sprints (sprintStart, sprintEnd) VALUES (?, ?)", ("2026-04-16", "2026-04-20"))
        cur.execute("INSERT OR IGNORE INTO sprints (sprintStart, sprintEnd) VALUES (?, ?)", ("2026-05-01", "2026-05-15"))
        cur.execute("INSERT OR IGNORE INTO sprints (sprintStart, sprintEnd) VALUES (?, ?)", ("2026-05-16", "2026-05-20"))
    else:
        print("Sprints already exist, skipping sprint creation.")

    # CREATE TICKETS
    if cur.execute("SELECT COUNT(*) FROM tickets").fetchone()[0] == 0:
        # Only insert if no tickets exist to avoid duplicates
        sprintID = cur.execute("SELECT sprintID FROM sprints").fetchall()
        for i in sprintID:
            cur.execute("INSERT OR IGNORE INTO tickets (sprintID, userID, descr, storyPoints) VALUES (?, ?, ?, ?)", (i[0], 1, f"Ticket {i[0]} Description", 5))
    else:
        print("Tickets already exist, skipping ticket creation.")

    cur.close()
    con.commit()
    con.close()

    