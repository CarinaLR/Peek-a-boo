import os
import json
import re
import requests
import datetime


from flask import Flask, session, render_template, redirect, request, flash, jsonify
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
            return render_template("error.html", message="please enter username")
        elif not request.form.get("password"):
            return render_template("error.html", message="plese enter password")

        # Access database.
        user = db.execute("SELECT * FROM users WHERE name = :username",
                          {"username": username})

        user_found = user.fetchone()

        # Check if user already exits.
        if user_found == None:
            return render_template("register.html", message="invalid user, please check your information.")

        # Remember user.
        session["user_id"] = user_found[0]
        session["user_name"] = user_found[1]

        # Redirect user to book-info page.
        return render_template("bookinfo.html", headline="Welcome, you are now logged in!")

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

    # Get information. request.args is used to return values of query string.
    title = request.args.get("book")
    # # .title() method returns a string where the first character in every word is upper case.
    # title = title.title()
    try:
        book_title = db.execute(
            "SELECT * FROM books WHERE isbn LIKE :title OR title LIKE :title OR author LIKE :title LIMIT 5", {"title": title})
        books = book_title.fetchall()
        return render_template("info.html", books=books)
    except ValueError:
        return render_template("error.html", message="we can't find books with that description.")

    # Make sure book exists.
    search_book = request.form.get(book_title)
    if search_book is None:
        return render_template("error.html", message="invalid title of the book.")
    else:
        return render_template("info.html", books=books)


@app.route("/book-page/<isbn>", methods=["GET", "POST"])
# Pass in isbn parameter.
def bookpage(isbn):
    # Set variables.
    headline = "Here is the information requested."

    if request.method == "POST":
        # Set user to be saved in reviews table.
        actual_user = session["user_id"]

        # Get information from user.
        review = request.form.get("review")
        rating = request.form.get("rating")

        # Use isbn parameter to get book info.
        row = db.execute(
            "SELECT isbn FROM books WHERE isbn = :isbn", {"isbn": isbn})

        # Storage book isbn.
        book_id = row.fetchone()
        book_id = book_id[0]

        # Confirm user review.
        user_review = db.execute("SELECT * FROM reviews WHERE user_id = :user_id AND book_isbn = :book_isbn", {
                                 "user_id": actual_user, "book_isbn": book_id})

        # Check if review already exists.
        if user_review.rowcount == 1:
            return render_template("error.html", message="Sorry, you already have a review for this book.")

        # Save rating.
        rating = int(rating)

        # Get current time.
        now = datetime.datetime.today()

        # Save all information in db.
        db.execute("INSERT INTO reviews (user_id, book_isbn, comment, rating, date) VALUES (:user_id, :book_isbn, :comment, :rating, :date)", {
                   "user_id": actual_user, "book_isbn": book_id, "comment": review, "rating": rating, "date": now})
        db.commit()

        return render_template("logout.html", headline="Your review have been submmitted.")
    else:
        # Get info and render.
        row = db.execute(
            "SELECT isbn, title, author, year FROM books WHERE isbn = :isbn", {"isbn": isbn})

        info = row.fetchall()

        # Read API key from env variable
        key = os.getenv("GOODREADS_KEY")
        res = requests.get("https://www.goodreads.com/book/review_counts.json",
                           params={"key": key, "isbns": isbn})
        if res.status_code != 200:
            raise Exception("ERROR: API request unsuccessful.")
        data = res.json()

        # Clear data to pass new info.
        data = data["books"][0]
        info.append(data)

        # Check by isbn
        row = db.execute(
            "SELECT isbn FROM books WHERE isbn = :isbn", {"isbn": isbn})

        bookinfo = row.fetchone()
        bookinfo = bookinfo[0]

        # Chechk book reviews
        res = db.execute(
            "SELECT users.name, comment, rating, to_char(date, 'YY Mon DD - HH24:MI:SS') as time FROM users INNER JOIN reviews ON users.id = reviews.user_id WHERE book_isbn = :book_isbn ORDER BY date", {"book_isbn": bookinfo})

        reviews = res.fetchall()

        return render_template("bookpage.html", headline=headline, bookinfo=info, reviews=reviews)


@app.route("/api/<isbn>", methods=["GET"])
# Pass in isbn parameter.
def api_json(isbn):
    # Read API isbn from db.
    local_db = db.execute(
        "SELECT isbn, title, author, year FROM books WHERE isbn = :isbn", {"isbn": isbn})
    info = local_db.fetchone()

    if local_db != None:
        # Read API key from env variable
        key = os.getenv("GOODREADS_KEY")
        goodreads_reviews = requests.get(
            "https://www.goodreads.com/book/review_counts.json", params={"key": key, "isbns": isbn})
        # Parse info from Goodreads api.
        work_ratings_count = goodreads_reviews.json(
        )['books'][0]['work_ratings_count']
        average_rating = goodreads_reviews.json()['books'][0]['average_rating']
        # JSON response format.
        data = {
            "title": info.title,
            "author": info.author,
            "year": info.year,
            "isbn": isbn,
            "review_count": work_ratings_count,
            "average_score": average_rating
        }
        # Render json response with described format. json.dumps() -convert Python object into a JSON string.
        response = json.dumps(data)
        return response
    else:
        return render_template("error.html", message="Sorry, your request status is 404 not found.")
