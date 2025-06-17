# Scrum board

This application provides a single interface to manage projects

# Tables
- Users: user ID, name and access level
- Logins (separate to users for security): user ID, password 
- Sprints: sprint ID, start date, end date
- Tickets: Ticket ID, sprint ID, userID

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
As an admin you can:
- View all users, tickets and sprints
- Create tickets, sprints and other admin users
- Delete tickets, sprints, and users

As a user you can:
- View all users, tickets and sprints
- Create tickets and sprints

You can also sign up as a regular user and gain standard functionality
