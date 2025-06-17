from flask import Flask
from auth.auth_route import auth_bp
from sprints.sprint_route import sprint_bp
from tickets.ticket_route import ticket_bp
from users.user_route import user_bp
from pages.page_route import page_bp
from db_init import createTables, initialValues
import secrets

app = Flask(__name__)
app.secret_key = secrets.token_hex(16)

createTables()
initialValues()

# Register Blueprints
app.register_blueprint(auth_bp)
app.register_blueprint(sprint_bp)
app.register_blueprint(ticket_bp)
app.register_blueprint(user_bp)
app.register_blueprint(page_bp)

if __name__ == '__main__':
    app.run(debug=False)
