import functools
import sqlite3

from flask import (Blueprint, flash, g, redirect, render_template, request, session, url_for, jsonify)

from werkzeug.security import check_password_hash, generate_password_hash

from flaskr.db import get_db

from flaskr.auth import login_required

bp = Blueprint('display', __name__)
from . import auth
# userID = session["user_id"]

@bp.route('/')
@login_required
def yourbooks():
    db = get_db()
    favorites = db.execute("SELECT books.title,  books.authors, books.publisher, books.average_rating, bookuser.comment, bookuser.rating FROM books, bookuser WHERE books.bookID = bookuser.bookID AND bookuser.userID = ?", (session["user_id"],))
    favorites = favorites.fetchall()
    # favorites = [list(favorite) for favorite in favorites]
    # favorites = favorites.comment
    # return favorites

    return render_template("index.html", favorites = favorites)
    # return f"{type(favorites)}"

    


