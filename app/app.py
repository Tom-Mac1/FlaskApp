from app import create_app
import os

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
