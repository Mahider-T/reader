DROP TABLE IF EXISTS users;
DROP TABLE IF EXISTS bookuser;


CREATE TABLE users(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT UNIQUE NOT NULL,
    password TEXT NOT NULL

);

CREATE TABLE books(
    bookID INTEGER PRIMARY KEY,
    title TEXT NOT NULL,
    authors TEXT NOT NULL,
    average_rating REAL DEFAULT 0,
    isbn TEXT,
    isbn13 TEXT,
    language_code TEXT,
    num_pages INTEGER,
    ratings_count INTEGER DEFAULT 0,
    text_reviews_count INTEGER DEFAULT 0,
    publication_date TEXT,
    publisher TEXT
);

CREATE TABLE bookuser(
    userID INTEGER REFERENCES users(id),
    bookID INTEGER REFERENCES books(bookID),
    rating INTEGER,
    comment TEXT,
    PRIMARY KEY (userID, bookID)
);

CREATE TABLE userfavorites(
    userID INTEGER REFERENCES users(id),
    bookID INTEGER REFERENCES books(bookID),
    PRIMARY KEY (userID, bookID)
);