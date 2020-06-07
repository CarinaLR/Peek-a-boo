# Set up db models -tables, columns & rows
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

# Adding db.Model in parentheses after class names indicates that these classes ‘inherit’ from db.Model.


class User(db.Model):
    __tablename__ = "users"
    _id = db.Column("id", db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    email = db.Column(db.String, nullable=False)
    password = db.Column(db.String, db.Integer, nullable=False)


class Book(db.Model):
    __tablename__ = "books"
    _id = db.Column("id", db.Integer, primary_key=True)
    isbn = db.Column("ISBN", db.Integer, nullable=False)
    title = db.Column("title", db.String)
    author = db.Column("author", db.String)
    year = db.Column("year", db.Integer)


class Review(db.Model):
    __tablename__ = "reviews"
    _id = db.Column("id", db.Integer, primary_key=True)
    user_id = db.Column("user_id", db.Integer,
                        db.ForeignKey("user.id"), nullable=False)
    book_id = db.Column("book_id", db.Integer,
                        db.ForeignKey("book.id"), nullable=False)
    comment = db.Column("comment", db.Text)
    rating = db.Column("rating", db.Integer)
    date = db.Column("date", db.Timestamp)
