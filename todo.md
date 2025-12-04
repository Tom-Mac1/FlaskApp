Most pressing
    - Unit testing
    - Linting
    - OWASP top 10 attacks, defend from 3
    - Hosting

Deployment
    Container:
    - Dockerise app
    - How does it work when using database with docker
    - Hosting solution what is available to free tier
    - Potential for kubernetes?
    - Integrate with ECS, Lambda, RDS

Done
    - Dropdown at top for what sprint
    - Shows dates next to "sprint: X"
    - TODO, In Progress, Done sections with tickets tiles (only show number and title)
    - Can drag and drop tickets (minor duplicating issue)
    - Add "state": TOdo, Doing, Done
    - Anything Doing or Done only shows in that sprint
    - Anything in ToDo should be accessible to all sprints
    - When moved to doing or done, updates db to reflect status
    - Default to sprints page
    - All buttons work via sprints page
    - Need to remove all references to page.home and make it page.sprints
    - When editing ticket, note sprint ID and load it in when going back
    - password hashing


Security considerations
    - passwords are hashed