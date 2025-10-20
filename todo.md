BIG IMPORTANT FIX
    - STOP THE DUPLICATION: when dragging and dropping tickets, sometimes up to 10 duplicates of 1 ticket can be made

UI:
    Sprints/Tickets:
    - pass sprint into loading sprint page for initial dropdown
    - when choose new sprint, reload page with different sprint passed in
    - remove delete button, put on edit page
    - edit page takes you back to the view sprints page (pass in sprint you were on)
    Users:
    - Add edit button
    - Edit should be done via popup rather than new page

DB:
    Sprints/Tickets

Deployment
    Container:
    - Docker for image
    - Hosting solution
    - How does it work when using database with docker
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