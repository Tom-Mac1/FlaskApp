from .auth import auth_bp
from .pages import page_bp
from .sprints import sprint_bp
from .tickets import ticket_bp
from .users import user_bp

all_bp = [auth_bp, page_bp, sprint_bp, ticket_bp, user_bp]
