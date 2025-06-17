from flask import Blueprint, render_template, request, session, flash, redirect, url_for
import sqlite3
from utils import get_access, get_users, get_sprints, get_tickets

page_bp = Blueprint('page', __name__)

@page_bp.route('/')
def index():
    return render_template('index.html')

@page_bp.route('/home')
def home():
    if session.get('user_id') == None:
        return render_template('index.html')
    return render_template('home.html')

@page_bp.route('/sprints')
def sprints():
    if session.get('user_id') == None:
        return render_template('index.html')
    else:
        connect = sqlite3.connect('FlaskAppDB.db')
        cursor = connect.cursor()
        cursor.execute('SELECT * FROM sprints')

        data = cursor.fetchall()
        return render_template("sprints.html", data=data, access=get_access())
    
@page_bp.route('/users')
def users():
    if session.get('user_id') == None:
        return render_template('index.html')
    else:
        connect = sqlite3.connect('FlaskAppDB.db')
        cursor = connect.cursor()
        cursor.execute('SELECT * FROM users')

        data = cursor.fetchall()
        return render_template("users.html", data=data, access=get_access())
    
@page_bp.route('/tickets')
def tickets():
    if session.get('user_id') == None:
        return render_template('index.html')
    else:
        print(get_access())
        connect = sqlite3.connect('FlaskAppDB.db')
        cursor = connect.cursor()
        cursor.execute('SELECT * FROM tickets')

        data = cursor.fetchall()
        return render_template("tickets.html", data=data, access=get_access())