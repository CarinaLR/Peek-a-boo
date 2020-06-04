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


# API Key
# key: FIbCP1B0yajXYRYbsLujng
# secret: zG93CWU1lNCz59RrU6NN57zA00eZcghAceTQfEIUzA
