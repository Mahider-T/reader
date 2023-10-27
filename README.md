# Flask Book Reviewing Application

## Description:
A simple Flask application to review books.

## Features:

`User Authentication:` Register and log in to access the full features of the website.
`Book Search:` Search for a book using the book title.
`Book Filter:` Filter books that match a given criteria.
`Book Rating:` Rate a book.
`Comment: ` Comment on a book.
`Showcase:` Display the most recently published books and top-rated books.

## Endpoints

### User Authentication

- `POST /auth/register`: Register a new user.
- `POST /auth/login`: Log in an existing user.
- `POST /auth/logout`: Log out the current user.

### Book Reviews
- `POST /books/addBook`: Add a new book to the DB.
- `POST /books/find`: Search for a book with title.
- `GET  /books/bookinfo/:id`: Get detailed information about a given book.
- `POST /comment/:id`: Comment on a given book.
- `POST /rate/:id`: Rate a given book.
- `GET /books/topbooks`: Display a list of top rated books.
- `POST books/filter:`: Filter books based on some criteria.


## Getting Started

### Project Structure

├── flaskr
│   ├── auth.py
│   ├── books.csv
│   ├── books.py
│   ├── db.py
│   ├── display.py
│   ├── flaskr.sqlite
│   ├── __init__.py
│   ├── __pycache__
│   │   ├── auth.cpython-310.pyc
│   │   ├── books.cpython-310.pyc
│   │   ├── db.cpython-310.pyc
│   │   ├── display.cpython-310.pyc
│   │   └── __init__.cpython-310.pyc
│   ├── schema.sql
│   ├── statics
│   │   └── style.css
│   ├── templates
│   │   ├── eachbook.html
│   │   ├── filter.html
│   │   ├── index.html
│   │   ├── layout.html
│   │   ├── login.html
│   │   ├── register.html
│   │   ├── searchresult.html
│   │   ├── topbooks.html
│   │   └── trending.html
│   └── tests
├── instance
│   └── flaskr.sqlite
├── README.md


### Prerequisites
        Python 3.0 or higher
        Flask
        SQLite database

### Installation
        Clone the repository git clone https://github.com/Mahider-T reader

### Run the application
        flask --app flaskr run
## Usage
        After running the server, open your web browser and visit http://localhost:5000 to start using the application.

