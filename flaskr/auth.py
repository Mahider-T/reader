import functools

from flask import (Blueprint, flash, g, redirect, render_template, request, session, url_for)

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
            finally:
                flash("Success!")
                return "Success!"
                return redirect(url_for("auth.login"))
        flash(error)

    return render_template('auth/register.html')    

@bp.route("/login", methods = ("GET", "POST"))
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        error = None
        db = get_db()

        if not username:
            error = "Username can not be empty."
        elif not password:
            error = "Password can not be empty."

        if error == None:
            row = db.execute("SELECT * FROM user WHERE username = ?", username).fetchone()
            
            if row is None:
                error = "No such user."
            elif not check_password_hash(row["password"], password):
                error = "Incorrect password"
            
            if error in None:
                session.clear()
                session['user_id'] = row['id']
                return redirect(url_for('index'))
        flash(error)
    return render_template('auth/login.html')

