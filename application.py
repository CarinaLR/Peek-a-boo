import os

from flask import Flask, session
from flask_session import Session
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

app = Flask(__name__)

# Check for environment variable
if not os.getenv("postgres://sqdsasjxjwxssg:1f55f88789b3dcb03e157286568e229506fa309e05e5f02e8aff751d7d63e3cd@ec2-54-86-170-8.compute-1.amazonaws.com:5432/dd25bg1thd4271"):
    raise RuntimeError("DATABASE_URL is not set")

# # Configure session to use filesystem
app.config["SQLALCHEMY_DATABASE_URI"] = True
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# # Set up database
engine = create_engine(os.getenv(
    "postgres://sqdsasjxjwxssg:1f55f88789b3dcb03e157286568e229506fa309e05e5f02e8aff751d7d63e3cd@ec2-54-86-170-8.compute-1.amazonaws.com:5432/dd25bg1thd4271"))
db = scoped_session(sessionmaker(bind=engine))


@app.route("/")
def index():
    return "Project 1: TODO"
