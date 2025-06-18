# Scrum board

This application provides a single interface to manage projects

# Tables
- Users: user ID, name and access level
- Logins (separate to users for security): user ID, password 
- Sprints: sprint ID, start date, end date
- Tickets: Ticket ID, sprint ID, userID, Description, Story Points

# How to use
Initialise a virtual environment:
```bash
cd /app
python3 -m venv venv 
venv/Scripts/activate
pip install -r requirements.txt
```
Run application: Database will auto populate initial values

```bash
flask run
```

# Functionality
As an <b>admin</b> you can:
- View all users, tickets and sprints
- Create tickets, sprints and other admin users
- Delete tickets, sprints, and users

As a <b>user</b> you can:
- View all users, tickets and sprints
- Create tickets and sprints

You can also sign up as a regular user and gain basic functionality

# Approach taken
- This uses a modular approach, with folders containing functionality for each aspect, such as users, auth, pages, etc
- Through this approach, app.py can be less clustered and adding/working on features can be done more efficiently

# Structure breakdown

## Directory
```
app/
├── app.py    
├── db
|   └── db-init.py  
├── routes
|   ├── Auth
|   |   ├── __init__.py
|   |   └── auth_route.py
|   ├── Pages
|   |   ├── __init__.py
|   |   └── page_route.py
|   ├── Sprints
|   |   ├── __init__.py
|   |   └── sprint_route.py
|   ├── Tickets
|   |   ├── __init__.py
|   |   └── ticket_route.py
|   └── Users
|       ├── __init__.py
|       └── user_route.py
├── Static
├── Templates
├── db
|   └── utils.py    
├── __init__.py
├── app.py
└── requirements.txt
```
# App.py
- Main file. Collates routes from all of the sub folders
    - ### Init.py
        - This combines the blueprints that are used to create the app

## Routes
- This folder breaks down the functionality into groups to make debugging/feature adding easier
    
    - ### Auth
        - Contains functionality for logging in, signing out and signing up
    - ### Pages
        - Contains functionality for loading pages with necessary checks and information
    - ### Sprints
        - Functionality to create or delete sprints

    - ### Tickets
        - Functionality to create or delete tickets

    - ### Users
        - User management (creation/deletion) and password reset

## Db
- Initialises the database, and adds temporary records if there are none

## Static
- Contains Javascript components 
    - ### Confirm.js
        - Contains functions that create a pop up asking the user to confirm their action before it will run

## Templates
- Contains all HTML pages that routes point to

## Utils
- Contains "Getter" functions that supply routes with information required for some of the pages