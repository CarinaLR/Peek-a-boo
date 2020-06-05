import os
import requests


from flask import Flask, session, render_template
from flask_session import Session
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

app = Flask(__name__)

# Check for environment variable
if not os.getenv("DATABASE_URL"):
    raise RuntimeError("DATABASE_URL is not set")

# Configure session to use filesystem
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Set up database
engine = create_engine(os.getenv(
    "DATABASE_URL"))
db = scoped_session(sessionmaker(bind=engine))


@app.route("/")
def index():
    headline = "Hello, welcome to Peek a boo!"
    return render_template("index.html", headline=headline)

# Route for Goodreads APIs reviews


@app.route("/reviews")
def main():
    res = requests.get("https://www.goodreads.com/book/review_counts.json",
                       params={"key": "FIbCP1B0yajXYRYbsLujng", "isbns": "0590396560"})
    if res.status_code != 200:
        raise Exception("ERROR: API request unsuccessful.")
    data = res.json()
    return data


@app.route("/sign-up")
def sign():
    headline = "Please enter your information below."
    return render_template("register.html", headline=headline)


@app.route("/login")
def login():
    headline = "Welcome, you are already login."
    return render_template("login.html", headline=headline)


@app.route("/logout")
def logout():
    headline = "Thank you for visiting us, come back soon!"
    return render_template("logout.html", headline=headline)


@app.route("/request")
def request():
    headline = "Enter the information requested to help you with your search."
    return render_template("request.html", headline=headline)


# API Key
# key: FIbCP1B0yajXYRYbsLujng
# secret: zG93CWU1lNCz59RrU6NN57zA00eZcghAceTQfEIUzA
