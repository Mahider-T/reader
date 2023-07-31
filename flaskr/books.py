import csv
import functools

from flask import (Blueprint, flash, g, redirect, render_template, request, session, url_for)

from werkzeug.security import check_password_hash, generate_password_hash

from flaskr.db import get_db

bp = Blueprint('books', __name__, url_prefix = '/books')

db = get_db()

def get_books_table_header():
    with open("books.csv", "r") as csvfile:

        reader = csv.reader(csvfile, skiprows = 1)
        return reader
        
# numberOfRows = len(get_books_table_header())

for row in reader:
    db.execute("INSERT INTO books VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",(row[0], row[1],row[2], row[3],row[4], row[5],row[6], row[7],row[8], row[9],row[10], row[11]))
    db.commit()
    
print(numberOfRows)