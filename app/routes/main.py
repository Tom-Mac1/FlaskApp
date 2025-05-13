import sqlite3
# Login
def login():
    con1 = sqlite3.connect("FlaskAppDB.db")
    cur1 = con1.cursor()
    cur1.execute("PRAGMA foreign_keys = ON;")
    username = input("Username: ")
    password = input("Password: ")
    idList = cur1.execute("SELECT userID FROM users WHERE name=?", (username,)).fetchone()
    if idList != None:
        id = idList[0]
    else:
        id = 0
    pw = cur1.execute("SELECT password FROM logins WHERE userID="+str(id)).fetchone()
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