import csv
import functools
import sqlite3

from flask import (Blueprint, flash, g, redirect, render_template, request, session, url_for, current_app,jsonify)

from werkzeug.security import check_password_hash, generate_password_hash

from flaskr.db import get_db

from flaskr.auth import login_required

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

globalvalue1 = None

@bp.route("/find", methods = ("GET", "POST"))
def find():
    if request.method == "POST":
        db = get_db()
        search = request.form.get("search")
        final = db.execute("SELECT title, bookID FROM books WHERE title LIKE ?", (f"%{search}%",))
        final = final.fetchall()  
        # results = [element for element in final]

        # return results
        # attr = [title for title in final] 
        # highlighted_titles = [title[0].replace(search, f"<mark>{search}</mark>") for title in final]
        # highlighted_titles = [f'<a href = "google.com">{title[0]}</a><br>' for title in final]
        
        # highlighted_titles = [f"</br>{title}</br>" for title in highlighted_titles]
        # return highlighted_titles
        return render_template("searchresult.html", results = final)
        # return "\n\n".join(highlighted_titles)
        # return [title for title in highlighted_titles]
        # titles = f"{type(titles[0])}"
        # titles = [title for title in titles]
        # return jsonify(attr)
@bp.route("/bookinfo/<int:id>")
def bookinfo(id):

    from . import auth
    userID = session["user_id"]

    db = get_db()
    result = db.execute("SELECT title, authors, average_rating,num_pages, publication_date, publisher, bookID FROM books WHERE bookID = ?", (id,)).fetchall()[0]
    personal = db.execute("SELECT comment FROM bookuser WHERE bookID = ? AND userID = ?", (id,userID,)).fetchone()
    
    if personal is not None:
        personal = personal[0]

    thisBook = {
        "title": result[0],
        "author": result[1],
        "average rating": result[2],
        "number of pages": result[3],
        "publication date": result[4],
        "publisher":result[5],
        "id": result[6],
        "your comment": personal
    }

    global globalvalue1 
    globalvalue1 = thisBook

    # return thisBook
    return render_template("eachbook.html", thisBook = thisBook)
    # return f"{personal}"
@bp.route("/comment/<int:id>", methods = ("GET", "POST", "PUT"))
def comment(id):
    from . import auth
    userID = session["user_id"]
    # if request.method == "GET":
    #     db = get_db()
    #     cursor = db.execute("SELECT * FROM bookuser WHERE bookID = ?", (id,))
    #     cursor = cursor.fetchall()
    #     return jsonify(cursor)
    if request.method == "POST":
        db = get_db()
        comment = request.form["comment"]

        # from . import auth
        # userID = session["user_id"]
        # 
        hasCommented = db.execute("SELECT comment FROM bookuser WHERE bookID = ? and userID = ?",(id,userID,)).fetchone()
        if hasCommented is None:
            db.execute("INSERT INTO bookuser (userID, bookID, comment) values (?,?,?)", (int(userID), id, comment,))
            db.commit()
        else:
            db.execute("UPDATE bookuser SET comment = ? WHERE userID = ? AND bookID = ?", (comment,userID,id))
            db.commit()
        updatedBook = db.execute("SELECT comment FROM bookuser WHERE bookID = ? and userID = ?",(id,userID,)).fetchall()

        # return updatedBook
        return redirect(url_for('books.bookinfo', id = id))
        # return render_template("eachbook.html", thisBook = globalvalue)
        
        # db.commit()
        # return f"{id} --- {userID} --- {comment}"
        # return hasCommented
    # else:
    #     db = get_db()
    #     comment = request.form["comment"]
    #     db.execute("UPDATE bookuser SET comment = ? WHERE userID = ? AND bookID = ?", (comment,int(userID), id,))
    #     db.commit()
    #     title = db.execute("SELECT title FROM books WHERE bookID = ?", (int(id),))
    #     title = title.fetchone()
    #     update = {
    #         "bookID": id,
    #         "title": title[0],
    #         "comment": comment 
    #     }
    #     return jsonify(update)

@bp.route("/rate/<int:id>", methods = ("GET", "POST", "PUT"))
def rate(id):
    from . import auth
    userID = session["user_id"]
    db = get_db()
    if request.method == "POST":
        rate = request.form["rate"]
        execution = db.execute("INSERT INTO bookuser (userID, bookID, rating) VALUES (?,?,?)", (userID, id, rate,))
        db.commit()
        rating = {
            "bookID": id,
            "rate" : rate
        }
        return jsonify(rating)

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
@bp.route("/topbooks")
def topbooks():
    db = get_db()
    results = db.execute("SELECT title, authors, average_rating, publication_date, publisher FROM books ORDER BY average_rating DESC, title ASC LIMIT 10;")
    # results = db.execute("SELECT title, average_rating FROM books ORDER BY average_rating DESC LIMIT 10;")
    results = results.fetchall()
    results = [result for result in results]
    # for item in results:
    #     if 
    return render_template("topbooks.html", results = results)
    # return result
@bp.route("/trending")
def trending():
    db = get_db()
    results = db.execute("SELECT title, authors, average_rating, publication_date, publisher FROM books ORDER BY publication_date DESC LIMIT 10;")
    results = results.fetchall()

    return render_template("trending.html", results = results)
# @bp.route("/myBooks")
# def myBooks():
#     db = get_db()
#     db.execute()

@bp.route("/filter", methods = ("GET", "POST"))
def filter():
    return "hi"


@bp.route("getUser")
@login_required
def getUser():
    # userID = session["user_id"]
    # return f"userid is {userID}"
    return "whatttaaaaa"



