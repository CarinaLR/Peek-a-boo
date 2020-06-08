import os
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
    id = 1

    # Clear session.
    session.clear()

    # Submitting a form via POST
    if request.method == "POST":

        # Check if info has an username
        if not request.form.get("username"):
            return render_template("register.html", message="must be register")

        # Access database for username
        userCheck = db.execute("SELECT * FROM users WHERE name = :username",
                               {"username": request.form.get("username")}).fetchone()

        # Check if username already exist
        if userCheck:
            return render_template("login.html", message="username already exist")

        # Check if info has a password
        elif not request.form.get("password"):
            return render_template("login.html", message="must be login")

        # Check if info has an email
        elif not request.form.get("email"):
            # Access database for email
            userEmail = db.execute("SELECT * FROM users WHERE email = :email",
                                   {"email": request.form.get("email")}).fetchone()
            if userEmail:
                return render_template("login.html", message="email already exist")

            return render_template("login.html", message="must be login")

        # Check passwords are equal
        elif not request.form.get("password") == request.form.get("password"):
            return render_template("register.html", message="passwords didn't match")

        # Insert info into database
        db.execute("INSERT INTO users (id, name, email, password) VALUES (:id,:username, :email, :password)",
                   {"id": id+1,
                    "username": request.form.get("username"),
                    "email": request.form.get("email"),
                    "password": request.form.get("password")})

        # Commit changes to database
        db.commit()

        flash('Account created', 'info')

        # Redirect user to login page
        return redirect("/login")

    # User reached route via redirect from Search botton.
    else:
        return render_template("register.html", headline=headline)


@app.route("/login", methods=["GET", "POST"])
def login():
    # Set variables.
    headline = "Welcome, you are not logged in!"
    return render_template("login.html", headline=headline)


@app.route("/logout")
def logout():
    headline = "Thank you for visiting us, come back soon!"
    session.pop("sign", None)
    session.pop("email", None)
    return render_template("logout.html", headline=headline)


@app.route("/book-info")
def bookinfo():
    headline = "Enter the information requested to help you with your search."
    return render_template("bookinfo.html", headline=headline)
