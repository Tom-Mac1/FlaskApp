# FlaskApp

- The goal of this app is a booking system with the following functionality
- Can create a user account, sign in and out of it
- Only admin users can delete data and create other admin users

# Other idea
- Scrum/agile board
- tickets, sprints
- can have sprintID, UserID records for tickets as foreign keys
- User MUST login/create account to start using the app
- Start app with admin user "root" and set pw
- Must change password when logging in root for first time
- Can view tickets by sprint or by user
- Can view dates tied to each sprint

# Code

Main.py
- flask
- core functionality 
- frontend
- login function
- call db.py when want to modify data or login etc

Db.py
- sqlite
- create database
- contain functions for modifying database

# Tables
- Table 1: user details (id as foreign key?)
- Table 2: passwords (uses id as primary key)
- Table 3: bookings data (Name, email etc)

# Agile

Come up with tickets
(as a user I want to be able to)
- create required databases in a python script
- create, retrieve, update and delete records in database via python
- create the admin user when the app is run for the first time
- automatically link password to correct user ID
- login as a user
- have only admin users be able to delete data

