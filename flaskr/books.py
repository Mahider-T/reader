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

@bp.route("/findbookattributes")
def find():
    db = get_db()
    find = request.form["find"]
    cursor = db.execute("SELECT * FROM books WHERE title LIKE ?", (f"%{find}%",))
    titles = cursor.fetchall()  
    attr = jsonify(titles)
    return attr
    # attr = [title for title in titles ] 
    # highlighted_titles = [title[0].replace("the", f"<mark>{find}</mark>") for title in titles]
    # highlighted_titles = [f"</br>{title}</br>" for title in highlighted_titles]

    # return "\n\n".join(highlighted_titles)
    # return [title for title in highlighted_titles]
    # titles = f"{type(titles[0])}"
    # titles = [title for title in titles]
    # return jsonify(attr)

@bp.route("/comment/<int:id>", methods = ("GET", "POST", "PUT"))
def comment(id):
    from . import auth
    userID = session["user_id"]
    if request.method == "GET":
        db = get_db()
        cursor = db.execute("SELECT * FROM bookuser WHERE bookID = ?", (id,))
        cursor = cursor.fetchall()
        return jsonify(cursor)
    if request.method == "POST":
        db = get_db()
        comment = request.form["comment"]

        # from . import auth
        # userID = session["user_id"]

        db.execute("INSERT INTO bookuser (userID, bookID, comment) values (?,?,?)", (int(userID), id, comment,))
        db.commit()
        return f"{id} --- {userID} --- {comment}"
    else:
        db = get_db()
        comment = request.form["comment"]
        db.execute("UPDATE bookuser SET comment = ? WHERE userID = ? AND bookID = ?", (comment,int(userID), id,))
        db.commit()
        title = db.execute("SELECT title FROM books WHERE bookID = ?", (int(id),))
        title = title.fetchone()
        update = {
            "bookID": id,
            "title": title[0],
            "comment": comment 
        }
        return jsonify(update)
        

@bp.route("/addbook", methods = ("GET", "POST"))
def addbook():
    if request.method == "POST":
        # bookID = request.form["bookID"]
        title = request.form["title"]
        author = request.form["author"]
        isbn = request.form["isbn"]
        isbn13 = request.form["isbn13"]

        db = get_db()
        db.execute("INSERT INTO books (title, authors, isbn, isbn13) VALUES (?,?,?,?)", (title, author, isbn,isbn13,))
        db.commit()

@bp.route("getUser")
def getUser():
    userID = session["user_id"]
    return f"username is {userID}"



