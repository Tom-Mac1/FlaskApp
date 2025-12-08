# from app import create_app
# import os

# app = create_app()
import os
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

app = create_app()
#app.config["SECRET_KEY"] = os.environ.get("SECRET_KEY")

app.config.update(
    SESSION_COOKIE_SECURE=True,
    SESSION_COOKIE_HTTPONLY=True,
    SESSION_COOKIE_SAMESITE="Lax"
)

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(debug=False,host="0.0.0.0", port=port)
