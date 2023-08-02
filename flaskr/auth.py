import functools
import sqlite3

from flask import (Blueprint, flash, g, redirect, render_template, request, session, url_for, jsonify)

from werkzeug.security import check_password_hash, generate_password_hash

from flaskr.db import get_db

bp = Blueprint('auth', __name__, url_prefix = '/auth')


@bp.route("/hello")
def hello():
    return "Hello!"

@bp.route('/register', methods = ('GET', 'POST'))
def register():
    if request.method == 'POST':
        username = request.form["username"]
        password = request.form["password"]
        error = None

        db = get_db()

        if not username:
            error = "Username can not be empty"
        elif not password:
            error = "Password can not be empty"
        
        if error is None:
            try:
                db.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, generate_password_hash(password)))
                db.commit()
            except db.IntegrityError:
                error = f"User {username} is already registered."
            else:
                # flash("Success!")
                return "Success!"
                # return redirect(url_for("auth.login"))
        flash(error)

    return render_template('auth/register.html')    

@bp.route("/login", methods = ("GET", "POST"))
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        error = None
        db = get_db()

        # if not username:
        #     error = "Username can not be empty."
        # elif not password:
        #     error = "Password can not be empty."

        # if error == None:
        row = db.execute("SELECT * FROM users WHERE username = ?", (username,)).fetchone()
        
        if row is None:
            error = "No such user."
        elif not check_password_hash(row['password'], password):
            error = "Incorrect password"
        
        if error is None:
            session.clear()
            session['user_id'] = row['id']
            # return redirect(url_for('books.find'))
            return "Successfully logged in!"
        flash(error)
    return render_template('auth/login.html')

@bp.route("/logout")
def logout():
    session.clear()
    return redirect(url_for('index'))

# function below makes only authenticated users use functionalities 
def login_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            return redirect(url_for('auth.login'))
        return view(**kwargs)
    return wrapped_view

