import csv
import os

from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker


# Set up database
engine = create_engine(os.getenv("DATABASE_URL"))
db = scoped_session(sessionmaker(bind=engine))


def main():
    # Create tables based on each table definition in `models`
    db.execute("CREATE TABLE users (id INTEGER PRIMARY KEY, name VARCHAR NOT NULL, email VARCHAR NOT NULL, password VARCHAR NOT NULL)")
    db.execute("CREATE TABLE books (isbn VARCHAR PRIMARY KEY,title VARCHAR NOT NULL,author VARCHAR NOT NULL,year VARCHAR NOT NULL)")
    db.execute("CREATE TABLE reviews (id INTEGER PRIMARY KEY, user_id INTEGER,book_isbn VARCHAR, CONSTRAINT user_id_fk FOREIGN KEY (user_id) REFERENCES users (id), CONSTRAINT book_isbn_fk FOREIGN KEY (book_isbn) REFERENCES books (isbn), comment VARCHAR, rating INTEGER NOT NULL, date TIMESTAMP NOT NULL)")
    f = open("books.csv")
    reader = csv.reader(f)
    for isbn, title, author, year in reader:
        db.execute("INSERT INTO books (isbn, title, author, year) VALUES (:isbn, :title, :author, :year)",
                   {"isbn": isbn, "title": title, "author": author, "year": year})
        print(f"Added book {isbn} , {title} by {author} published on {year}.")
        print("done")
    db.commit()


if __name__ == "__main__":
    main()
