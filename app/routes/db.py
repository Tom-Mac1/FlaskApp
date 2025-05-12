import sqlite3
con = sqlite3.connect("FlaskAppDB.db")
cur = con.cursor
# Table 1: user details (id as foreign key?)
cur.execute("CREATE TABLE users(name, email, id)")
# Table 2: passwords (uses id as primary key)
cur.execute("CREATE TABLE login(id, password)")
# Table 3: 
cur.execute("CREATE TABLE users(name, email, id)")