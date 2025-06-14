from flask import Flask, render_template, request, redirect, url_for, flash
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from models import db, Book, Note, User
from datetime import date
from sqlalchemy.sql import extract
from collections import Counter
from calendar import month_name

# app config
app = Flask(__name__)
app.config['SECRET_KEY'] = 'dev'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///books.db'
db.init_app(app)

# login setup
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'  # redirects to this view if not logged in

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# routes

# redirect root
@app.route('/')
def root():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    else:
        return redirect(url_for('login'))

# auth routes

@app.route('/register', methods=['GET', 'POST'])
def register():
    # register new users
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if User.query.filter_by(username=username).first():
            flash('Username already exists')
            return redirect(url_for('register'))
        user = User(username=username)
        user.set_password(password)
        db.session.add(user)
        db.session.commit()
        return redirect(url_for('login'))
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    # log users in
    if request.method == 'POST':
        user = User.query.filter_by(username=request.form['username']).first()
        if user and user.check_password(request.form['password']):
            login_user(user)
            return redirect(url_for('home'))
        flash('Invalid username or password')
    return render_template('login.html')

@app.route('/logout')
@login_required
def logout():
    # log users out
    logout_user()
    return redirect(url_for('login'))

# book views

@app.route('/home')
@login_required
def home():
    # show all books
    books = Book.query.filter_by(user_id=current_user.id).order_by(Book.id.desc()).all()
    return render_template('home.html', books=books)

@app.route('/current')
@login_required
def current():
    # show only books currently being read
    books = Book.query.filter_by(user_id=current_user.id).filter(Book.finished.is_(False)).order_by(Book.id.desc()).all()
    return render_template('current.html', books=books)

@app.route('/finished')
@login_required
def finished():
    # show only finished books
    books = Book.query.filter_by(user_id=current_user.id).filter(Book.finished.is_(True)).order_by(Book.id.desc()).all()
    return render_template('finished.html', books=books)

# book management

@app.route('/addb', methods=["POST"])
@login_required
def book():
    # add a new book
    title = request.form.get("title")
    author = request.form.get("author")
    new_book = Book(title=title, author=author, user_id=current_user.id)
    db.session.add(new_book)
    db.session.commit()
    return redirect('/')

@app.route('/deleteb/<int:id>')
@login_required
def delete_book(id):
    # delete a book
    book = Book.query.get(id)
    db.session.delete(book)
    db.session.commit()
    return redirect('/')

# note management

@app.route('/deleten/<int:id>')
@login_required
def delete_note(id):
    # delete a note
    note = Note.query.get(id)
    db.session.delete(note)
    db.session.commit()
    return redirect(url_for('book_details', book_id=note.book_id))

# book details

@app.route('/book/<int:book_id>', methods=['GET', 'POST'])
@login_required
def book_details(book_id):
    # view book details and add a note
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
            return redirect(url_for('book_details', book_id=book.id))
    return render_template('book_details.html', book=book)

# book status

@app.route('/book/<int:book_id>/finish', methods=['POST'])
@login_required
def mark_as_finished(book_id):
    # mark book as finished
    book = Book.query.get_or_404(book_id)
    book.finished = True
    book.finish_date = date.today()
    db.session.commit()
    return redirect(url_for('book_details', book_id=book.id))

@app.route('/book/<int:book_id>/current', methods=['POST'])
@login_required
def mark_as_current(book_id):
    # mark book as currently reading
    book = Book.query.get_or_404(book_id)
    book.finished = False
    book.finish_date = None
    db.session.commit()
    return redirect(url_for('book_details', book_id=book.id))

# stats page

@app.route('/stats', methods=['GET'])
@login_required
def stats():
    # show reading stats for selected year
    current_year = date.today().year
    years = list(range(current_year, current_year - 10, -1))
    selected_year = request.args.get('year', default=str(current_year))

    books = Book.query.filter_by(user_id=current_user.id)\
        .filter(extract('year', Book.finish_date) == selected_year)\
        .order_by(Book.id.desc()).all()

    bookscol1 = books[::2]
    bookscol2 = books[1::2]

    month_counts = Counter(book.finish_date.month for book in books)
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

# create db tables
with app.app_context():
    db.create_all()

# run the app
if __name__ == '__main__':
    app.run(debug=True)
