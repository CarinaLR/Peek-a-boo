# Set up db models -tables, columns & rows
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

# Adding db.Model in parentheses after class names indicates that these classes ‘inherit’ from db.Model.


class User(db.Model):
    __tablename__ = "users"
    _id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.Varchar, nullable=False)
    email = db.Column(db.Varchar, nullable=False)
    password = db.Column(db.Varchar, nullable=False)


class Book(db.Model):
    __tablename__ = "books"
    isbn = db.Column("isbn", db.Varchar, primary_key=True)
    title = db.Column("title", db.Varchar, nullable=False)
    author = db.Column("author", db.Varchar, nullable=False)
    year = db.Column("year", db.Varchar, nullable=False)


class Review(db.Model):
    __tablename__ = "reviews"
    _id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column("user_id", db.Integer,
                        db.ForeignKey("user.id"))
    book_isbn = db.Column("book_isbn", db.Integer,
                          db.ForeignKey("book.isbn"))
    comment = db.Column("comment", db.Varchar)
    rating = db.Column("rating", db.Integer, nullable=False)
    date = db.Column("date", db.Timestamp)
