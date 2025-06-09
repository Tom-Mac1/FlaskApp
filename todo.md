# Priority items
- Add tickets
- Admin homepage (delete options, admin can create users)
- Delete functionality
- Create functionality
- Input validation (start date before end, sprint must end before new sprint)

# Add the following pages
- create tickets

# Update all pages to look nicer
- create custom css for it

# Functionality ticket items
- Pop up message for welcome, or invalid login
- Pop up message for user created
- Input validation
- Password rules/constraints
- create sprints
- create tickets
- Add a button to tickets page for assigning a user
- Add a button on sprints to view participants
- View tickets by sprint or user
- Set so only admin user can create other admin users
- Set so only admin user can delete sprints/tickets
- Create button in sprints page that allows editing a specific sprint

# Extra bits
- Documentation for app design
- Documentation for DB relationships
- Create a mini sprint to demonstrate agile working

# Notes/Direction
- Security: cannot add /home or /sprints etc into url, must have active session
- Security: PW in separate db, add hashing though

# Add an adminHome page that has option to create admin user, delete items
# Use flask session to store user ID and name, validate before changing pages
#   Have a separate functionality on home page for admins
#   If no active session, re route to index (avoid being able to type "/home" in URL for example)
# Use flash to display messages to user
