BookTracker is a full-stack Flask web application that helps users keep track of the books they’re reading, finished, and taking notes on — with user authentication, CRUD functionality, and reading stats over time.

Features:
User Authentication (Register, Login, Logout)
Add & Manage Books with titles, authors, and statuses
Track Reading Progress (currently reading or finished)
Add Notes to individual books (chapter, page, content)
Visualize Stats for books finished per month/year
SQLite Database via SQLAlchemy
Secure Login Flow using Flask-Login

App Pages:
/register – Sign up for a new account
/login – Log in as an existing user
/home – View all books you've added
/current – View books currently being read
/finished – View finished books
/book/<id> – View details + notes for a specific book
/stats – Bar chart of books finished per month/year

Tech Stack:
Backend: Python, Flask, Flask-Login, SQLAlchemy
Frontend: HTML (Jinja templates), CSS
Database: SQLite

