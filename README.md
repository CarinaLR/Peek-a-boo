# Peek-a-boo!

A book review website.

Project 1 - Web Programming with Python and JavaScript

Built with `Python`/`SQLAlchemy`/
`Flask`/`PostgreSQL` database hosted by `Heroku` / `Goodreads API`.

## Setup

```
# application.py -the core of the project structure, connects the app with the database, and creates routes for each web page.
# import.py -takes the list of books from the .csv file and populates the books table in the database. This file also creates the users, books, and reviews tables for the database.
# models.py -gives a perspective of how each table of the database looks like and what data types are referring to.
# templates folder -contains all HTML files.
# static folder -contains CSS folder with the stylesheet and also img folder with all images using in this project.

```

## Enviroment

- `$ . venv/bin/activate`
- `export FLASK_APP=application.py`
- `export "DATABASE_URL"`
- `export "GOODREADS_KEY"`
- `flask run`

![](/static/img/welcome.png)

![](/static/img/registration.png)

![](/static/img/login.png)

![](/static/img/book_search.png)

![](/static/img/book_info.png)

![](/static/img/book_page0.png)

![](/static/img/book_page1.png)

![](/static/img/logout.png)
