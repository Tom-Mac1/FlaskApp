UI:
    - Default to sprints page
    - Move View users button to top of menu instead of home

    Sprints/Tickets:
    - Pass default sprint into sprints page to show
    - remove delete ticket button, put on edit page
    Users:
    - Add edit button

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