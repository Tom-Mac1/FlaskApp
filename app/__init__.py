from flask import Flask
import secrets
from app.routes import all_bp
from app.db.db_init import createTables, initialValues

def create_app():
    app = Flask(__name__)
    app.secret_key = secrets.token_hex(16)

    createTables()
    initialValues()

    for route in all_bp:
        app.register_blueprint(route)

    return app
