from flask import Flask, request
import sqlite3

app = Flask(__name__)

def create_connection():
    conn = sqlite3.connect('books.db')
    return conn

@app.route('/')
def home():
    return "Hello there"
@app.route("/addrec", methods = ['POST', 'GET'])
def addrec():
    if request.method == "POST":
        id = request.form["id"]
        name = request.form["name"]
        author = request.form["author"]
        rating = request.form["rating"]
        
        conn = sqlite3.connect('books.db')
        cur = conn.cursor()

        cur.execute("INSERT INTO books VALUES (?, ?, ?, ?)", (id, name, author, rating))
        conn.commit()

        return "Correct!"

if __name__ == "__main__":
    app.run() 