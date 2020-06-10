import os
import json
import re
import requests


from flask import Flask, session, render_template, redirect, request, flash
from flask_session import Session
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker


app = Flask(__name__)

# Check for environment variable
if not os.getenv("DATABASE_URL"):
    raise RuntimeError("DATABASE_URL is not set")

# Tell Flask what SQLAlchemy database to use.
app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("DATABASE_URL")
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

# Configure session to use filesystem
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Set up database
engine = create_engine(os.getenv(
    "DATABASE_URL"))
db = scoped_session(sessionmaker(bind=engine))


# Home page route


@app.route("/")
def index():
    headline = "Hello, welcome to Peek a boo!"
    return render_template("index.html", headline=headline)

# Route for Goodreads APIs reviews


@app.route("/reviews")
def goodreads():
    # Read API key from env variable
    key = os.getenv("GOODREADS_KEY")
    res = requests.get("https://www.goodreads.com/book/review_counts.json",
                       params={"key": key, "isbns": "0590396560"})
    if res.status_code != 200:
        raise Exception("ERROR: API request unsuccessful.")
    data = res.json()
    return data

# Application routes


@app.route("/sign-up", methods=["POST", "GET"])
def signup():
    # Set variables.
    headline = "Please enter your information below."
    username = request.form.get('username')
    email = request.form.get('email')
    password = request.form.get('password')

    # Clear session.
    session.clear()

    # Submit form.
    if request.method == "POST":

        # Check if info has an username
        if not request.form.get("username"):
            return render_template("register.html", message="must be registered")

        # Access database for username
        userCheck = db.execute("SELECT * FROM users WHERE name = :username",
                               {"username": request.form.get("username")}).fetchone()

        # Check if username already exist
        if userCheck:
            return render_template("login.html", message="username already exist")

        # Check if info has a password
        elif not request.form.get("password"):
            return render_template("login.html", message="please enter password")

        # Check if info has an email
        elif not request.form.get("email"):
            # Access database for email
            userEmail = db.execute("SELECT * FROM users WHERE email = :email",
                                   {"email": request.form.get("email")}).fetchone()
            if userEmail:
                return render_template("login.html", message="email already exist")

            return render_template("login.html", message="must be login")

        # Check password.
        elif not request.form.get("password") == request.form.get("password"):
            return render_template("register.html", message="invalid password")

        # Insert info into database.
        db.execute("INSERT INTO users (name, email, password) VALUES (:username, :email, :password)",
                   {
                       "username": request.form.get("username"),
                       "email": request.form.get("email"),
                       "password": request.form.get("password")})

        # Commit changes to database.
        db.commit()

        flash('Submitted info saved')

        # Redirect user to login page.
        return redirect("/login")

    # Renders registration page by clicking on Search button.
    else:
        return render_template("register.html", headline=headline)


@app.route("/login", methods=["GET", "POST"])
def login():
    # Set variables.
    headline = "Welcome, you are not logged in!"
    username = request.form.get("username")

    # Clear session.
    session.clear()

    # Submit a form.
    if request.method == "POST":

        # Check info from user.
        if not request.form.get("username"):
            return render_template("index.html", message="please enter username")
        elif not request.form.get("password"):
            return render_template("index.html", message="plese enter password")

        # Access database.
        user = db.execute("SELECT * FROM users WHERE name = :username",
                          {"username": username})

        result = user.fetchone()

        # Check if user already exits.
        if result == None:
            return render_template("register.html", message="invalid user, please check your information.")

        # Remember user.
        session["user_id"] = result[0]
        session["user_name"] = result[1]

        # Redirect user to book-info page.
        return redirect("/book-info")

    # Renders login page.
    else:
        return render_template("login.html", headline=headline)


@app.route("/logout")
def logout():
    headline = "Thank you for visiting us, come back soon!"
    # Clear seesion.
    session.clear()
    # Renders logout page, redirecting user to login page by login button.
    return render_template("logout.html", headline=headline)


@app.route("/book-info", methods=["GET"])
def bookinfo():
    # Set variables.
    headline = "Enter the information requested to help you with your search."

    # Get informatio.
    title = request.form.get("book")
    try:
        book_title = db.execute(
            "SELECT title FROM books WHERE title LIKE :title", {"title": title})
        books = book_title.fetchone()
    except ValueError:
        return render_template("error.html", message="we can't find books with that description.")

    # Make sure book exists.
    search_book = request.form.get(book_title)
    if search_book is None:
        return render_template("error.html", message="invalid title of the book.")
    else:
        return render_template("info.html", books=books)


# @app.route("/info")
# def info():
#     headline = "Book Description."
#     return render_template("info.html", headline=headline)


@app.route("/book-page")
def bookpage():
    headline = "Here is the information requested."
    return render_template("bookpage.html", headline=headline)
