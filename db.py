import sqlite3

conn = sqlite3.connect("books.db")

conn.execute("CREATE table books(id INTEGER, name TEXT, author TEXT, rating REAL)")
print("Table created successfully!")
conn.close()