import csv
import functools
import sqlite3

from flask import (Blueprint, flash, g, redirect, render_template, request, session, url_for, current_app,jsonify)

from werkzeug.security import check_password_hash, generate_password_hash

from flaskr.db import get_db

bp = Blueprint('books', __name__, url_prefix = '/books')
        
#The below route was used to initialize the books table for the first time by reading from a csv file
# @bp.route("/add")
# def add_books():
#     db = get_db()
#     with open("/home/oogway/reader/flaskr/books.csv", "r") as csvfile:
#         reader = csv.reader(csvfile)
#         next(reader, None)
#         for row in reader:
            # db.execute("INSERT INTO books VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",(row[0], row[1], row[2], row[3], row[4], row[5],row[6], row[7], row[8], row[9], row[10], row[11]))
#             db.commit()
#     return "Succuss!"

@bp.route("/find")
def find():
    db = get_db()
    find = request.form["find"]
    cursor = db.execute("SELECT title FROM books WHERE title LIKE ?", (f"%{find}%",))
    titles = cursor.fetchall()

    highlighted_titles = [title[0].replace("the", f"<mark>{find}</mark>") for title in titles]
    highlighted_titles = [f"</br>{title}</br>" for title in highlighted_titles]

    return "\n\n".join(highlighted_titles)
    # return [title for title in highlighted_titles]
    # return titles

@bp.route("/comment")
def comment():
    db = get_db()
    comment = request.form["comment"]
    from . import auth
    userID = session["user_id"]
    # username = db.execute("SELECT username FROM users WHERE id = ?", session["user_id"])
    bookID = request.form["bookID"]
    rating = request.form["rating"]
    # userid = request.form["userid"]
    db.execute("INSERT INTO bookuser (userID, bookID, rating, comment)values (?,?,?,?)", (int(userID), bookID, rating, comment,))
    db.commit()
    return f"{userID}"

@bp.route("getUser")
def getUser():
    userID = session["user_id"]
    return f"username is {userID}"



