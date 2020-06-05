# Set up db models -tables, columns & rows
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class User(db.Model):
    __tablename__ = "users"
    _id = db.Column("id", db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    email = db.Column(db.String, nullable=False)
    password = db.Column(db.String, db.Integer, nullable=False)


class Book(db.Model):
    __tablename__ = "books"
    _id = db.Column("id", db.Integer, primary_key=True)
    ISBN = db.Column("ISBN", db.Integer, nullable=False)
    title = db.Column("title", db.String)
    author = db.Column("author", db.String)
    publication_year = db.Column("publication_year", db.Integer)
