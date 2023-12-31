import csv
import functools
import sqlite3
import datetime

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
        return render_template("searchresult.html", results = final)
    
        # results = [element for element in final]

        # return results
        # attr = [title for title in final] 
        # highlighted_titles = [title[0].replace(search, f"<mark>{search}</mark>") for title in final]
        # highlighted_titles = [f'<a href = "google.com">{title[0]}</a><br>' for title in final]
        
        # highlighted_titles = [f"</br>{title}</br>" for title in highlighted_titles]
        # return highlighted_titles
        
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
    personal = db.execute("SELECT comment,rating FROM bookuser WHERE bookID = ? AND userID = ?", (id,userID,)).fetchone()
    comment = ""
    rating = ""
    if personal is not None:
        comment = personal[0]
        rating = personal[1]

    thisBook = {
        "title": result[0],
        "author": result[1],
        "average rating": result[2],
        "number of pages": result[3],
        "publication date": result[4],
        "publisher":result[5],
        "id": result[6],
        "your comment": comment,
        "your rating": rating
    }

    global globalvalue1 
    globalvalue1 = thisBook

    return render_template("eachbook.html", thisBook = thisBook)

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
        hasCommented = db.execute("SELECT comment FROM bookuser WHERE bookID = ? and userID = ?",(id,userID,)).fetchone()
        if hasCommented is None:
            db.execute("INSERT INTO bookuser (userID, bookID, comment) values (?,?,?)", (int(userID), id, comment,))
            db.commit()
        else:
            db.execute("UPDATE bookuser SET comment = ? WHERE userID = ? AND bookID = ?", (comment,userID,id))
            db.commit()
        updatedBook = db.execute("SELECT comment FROM bookuser WHERE bookID = ? and userID = ?",(id,userID,)).fetchall()

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
        rate = int(request.form["rate"])
        check = db.execute("SELECT * FROM bookuser WHERE userID = ? AND bookID = ?", (userID, id,)).fetchone()
        if not check:
            db.execute("INSERT INTO bookuser (userID, bookID, rating) values (?,?,?)", (userID, id, rate,))
            db.commit()
        else:
            execution = db.execute("UPDATE bookuser SET rating = ? WHERE userID = ? AND bookID = ? ", (rate, userID, id,))
            db.commit()
        return redirect(url_for('books.bookinfo', id = id))

@bp.route("/addbook", methods = ("GET", "POST"))
def addbook():
    if request.method == "POST":
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
    results = db.execute("SELECT title, authors, average_rating, publication_date, publisher, bookID FROM books ORDER BY average_rating DESC, title ASC LIMIT 10;")
    results = results.fetchall()
    results = [result for result in results]
    return render_template("topbooks.html", results = results)
    
@bp.route("/trending")
def trending():
    db = get_db()
    results = db.execute("SELECT title, authors, average_rating, publication_date, publisher, bookID FROM books ORDER BY publication_date DESC LIMIT 20;")
    results = results.fetchall()

    return render_template("trending.html", results = results)

@bp.route("/filter", methods = ("GET", "POST"))
def filter():
    today = datetime.date.today()
    
    min_rating = request.args.get('min_rating')
    max_rating = request.args.get('max_rating')
    min_pages = request.args.get('min_pages')
    max_pages = request.args.get('max_pages')
    start_date = request.args.get('start_date')
    end_date = request.args.get('end_date')

    if not end_date:    
        end_date = today.strftime('%Y-%m-%d')

    db = get_db()
    if min_rating is None:
        return render_template("filter.html")
    else:
        result = db.execute("SELECT bookID, title FROM books WHERE average_rating BETWEEN ? AND ? AND num_pages BETWEEN ? AND ? AND publication_date > ? AND publication_date < ?",(float(min_rating), float(max_rating), int(min_pages), int(max_pages),start_date,end_date)).fetchall()
        return render_template("filter.html", results = result)




