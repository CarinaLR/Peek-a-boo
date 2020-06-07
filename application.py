import os
import requests


from flask import Flask, session, render_template, request, flash
from flask_session import Session
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
# Import table definitions.
# from models import *

app = Flask(__name__)

# Check for environment variable
if not os.getenv("DATABASE_URL"):
    raise RuntimeError("DATABASE_URL is not set")

# Tell Flask what SQLAlchemy database to use.
# app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("DATABASE_URL")
# app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

# Configure session to use filesystem
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Set up database
engine = create_engine(os.getenv(
    "DATABASE_URL"))
db = scoped_session(sessionmaker(bind=engine))

# Link the Flask app with the database.
# db.init_app(app)


# def main():
#     # Create tables based on each table definition in `models`
#     db.create_all()

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
def sign():
    headline = "Please enter your information below."
    email = None
    if "sign" in session:
        sign = session["sign"]

        if request.method == "POST":
            email = request.form["email"]
            session["email"] = email
            flash("Email was saved!")
    else:
        if "email" in session:
            email = session["email"]
    return render_template("register.html", headline=headline, email=email)


@app.route("/login")
def login():
    headline = "Welcome, you are not logged in!"
    return render_template("login.html", headline=headline)


@app.route("/logout")
def logout():
    headline = "Thank you for visiting us, come back soon!"
    session.pop("sign", None)
    session.pop("email", None)
    return render_template("logout.html", headline=headline)


@app.route("/request")
def request():
    headline = "Enter the information requested to help you with your search."
    return render_template("request.html", headline=headline)
