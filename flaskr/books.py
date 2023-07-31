import csv
import functools

from flask import (Blueprint, flash, g, redirect, render_template, request, session, url_for)

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
#             db.execute("INSERT INTO books VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",(row[0], row[1], row[2], row[3], row[4], row[5],row[6], row[7], row[8], row[9], row[10], row[11]))
#             db.commit()
#     return "Succuss!"


@bp.route("/hi")
def hi():
    return "hi"
# print(numberOfRows)