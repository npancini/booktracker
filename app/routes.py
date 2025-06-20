from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_user, logout_user, login_required, current_user
from datetime import date
from sqlalchemy.sql import extract
from collections import Counter
from calendar import month_name

from app.models import db, Book, Note, User

# Blueprint for all routes
routes = Blueprint('routes', __name__)

# Redirect root to login or home
@routes.route('/')
def root():
    if current_user.is_authenticated:
        return redirect(url_for('routes.home'))
    return redirect(url_for('routes.login'))

# User registration
@routes.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if User.query.filter_by(username=username).first():
            flash('Username already exists')
            return redirect(url_for('routes.register'))
        user = User(username=username)
        user.set_password(password)
        db.session.add(user)
        db.session.commit()
        return redirect(url_for('routes.login'))
    return render_template('register.html')

# User login
@routes.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        user = User.query.filter_by(username=request.form['username']).first()
        if user and user.check_password(request.form['password']):
            login_user(user)
            return redirect(url_for('routes.home'))
        flash('Invalid username or password')
    return render_template('login.html')

# User logout
@routes.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('routes.login'))

# View all books
@routes.route('/home')
@login_required
def home():
    books = Book.query.filter_by(user_id=current_user.id).order_by(Book.id.desc()).all()
    return render_template('home.html', books=books)

# View books currently being read
@routes.route('/current')
@login_required
def current():
    books = Book.query.filter_by(user_id=current_user.id, finished=False).order_by(Book.id.desc()).all()
    return render_template('current.html', books=books)

# View finished books
@routes.route('/finished')
@login_required
def finished():
    books = Book.query.filter_by(user_id=current_user.id, finished=True).order_by(Book.id.desc()).all()
    return render_template('finished.html', books=books)

# Add a new book
@routes.route('/addb', methods=["POST"])
@login_required
def book():
    title = request.form.get("title")
    author = request.form.get("author")
    new_book = Book(title=title, author=author, user_id=current_user.id)
    db.session.add(new_book)
    db.session.commit()
    return redirect(url_for('routes.home'))

# Delete a book
@routes.route('/deleteb/<int:id>')
@login_required
def delete_book(id):
    book = Book.query.get(id)
    db.session.delete(book)
    db.session.commit()
    return redirect(url_for('routes.home'))

# Delete a note
@routes.route('/deleten/<int:id>')
@login_required
def delete_note(id):
    note = Note.query.get(id)
    db.session.delete(note)
    db.session.commit()
    return redirect(url_for('routes.book_details', book_id=note.book_id))

# View book details and add a note
@routes.route('/book/<int:book_id>', methods=['GET', 'POST'])
@login_required
def book_details(book_id):
    book = Book.query.get_or_404(book_id)
    if request.method == 'POST':
        form_id = request.form['form_id']
        if form_id == 'note':
            chapter = request.form['chapter']
            page = request.form['page']
            content = request.form['content']
            new_note = Note(
                chapter=chapter,
                page=page,
                content=content,
                book=book,
                user_id=current_user.id
            )
            db.session.add(new_note)
            db.session.commit()
            return redirect(url_for('routes.book_details', book_id=book.id))
    return render_template('book_details.html', book=book)

# Mark a book as finished
@routes.route('/book/<int:book_id>/finish', methods=['POST'])
@login_required
def mark_as_finished(book_id):
    book = Book.query.get_or_404(book_id)
    book.finished = True
    book.finish_date = date.today()
    db.session.commit()
    return redirect(url_for('routes.book_details', book_id=book.id))

# Mark a book as currently reading
@routes.route('/book/<int:book_id>/current', methods=['POST'])
@login_required
def mark_as_current(book_id):
    book = Book.query.get_or_404(book_id)
    book.finished = False
    book.finish_date = None
    db.session.commit()
    return redirect(url_for('routes.book_details', book_id=book.id))

# Stats dashboard
@routes.route('/stats', methods=['GET'])
@login_required
def stats():
    current_year = date.today().year
    years = list(range(current_year, current_year - 10, -1))
    selected_year = request.args.get('year', default=str(current_year))

    books = Book.query.filter_by(user_id=current_user.id)\
        .filter(extract('year', Book.finish_date) == selected_year)\
        .order_by(Book.id.desc()).all()

    bookscol1 = books[::2]
    bookscol2 = books[1::2]

    month_counts = Counter(book.finish_date.month for book in books if book.finish_date)
    labels = [month_name[i] for i in range(1, 13)]
    data = [month_counts.get(i, 0) for i in range(1, 13)]

    return render_template('stats.html',
        labels=labels,
        data=data,
        bookscol1=bookscol1,
        bookscol2=bookscol2,
        years=years,
        selected_year=selected_year,
        count=len(books)
    )