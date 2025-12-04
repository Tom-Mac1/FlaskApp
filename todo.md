Most pressing
    - Unit testing
    - Hosting

Note
    - SQLite is ok but not great at scale
    - Alternative would be to migrate to SQLAlchemy if the demand were to pick up

Deployment
    - render

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
    A01:2021: Broken Access Control
    - admin check for delete sprint
    - all actions validate user sessions

    A02:2021: Cryptographic Failures
    - all sensitive data (only passwords) is hashed
    - render automatically uses https, protects: login forms, session cookies, all user data
    - secure cookies: 
        SESSION_COOKIE_SECURE = True       # only send cookie over HTTPS
        SESSION_COOKIE_HTTPONLY = True     # JS cannot access the cookie
        SESSION_COOKIE_SAMESITE = 'Lax'    # defend against CSRF
    - no tokens etc to encrypt

    A03:2021-Injection
    - parameter binding: When using bind parameters, the database treats the input as data rather than executable code
        ie cur1.execute("SELECT password_hashed FROM logins WHERE userID=?", (str(id))) rather than "+str(id)"
    - sanitise all inputs before touching database
    - auto escaping in template files avoids executables being injected via database

    A05:2021-Security Misconfiguration
    - error messages are only plaintext standardised messages with no risk of outputting database information
    - debug disabled
    - cookies only over https

    A06:2021-Vulnerable and Outdated Components
    - up to date requirements.txt with relevant versions to avoid versions with known CVEs
    - version range given
