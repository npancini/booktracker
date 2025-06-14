from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

db = SQLAlchemy()

# user model handles login and keeps track of their books and notes
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), unique=True, nullable=False)
    password_hash = db.Column(db.String(256), nullable=False)
    books = db.relationship('Book', backref='user', cascade='all, delete-orphan')
    notes = db.relationship('Note', backref='user', cascade='all, delete-orphan')

    def set_password(self, password):
        # hashes the password
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password):
        # checks the password
        return check_password_hash(self.password_hash, password)

# book model for tracking books the user is reading or finished
class Book(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(80), nullable=False)
    author = db.Column(db.String(80), nullable=False)
    finished = db.Column(db.Boolean, default=False)
    finish_date = db.Column(db.Date, nullable=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    notes = db.relationship('Note', backref='book', cascade='all, delete-orphan')

# note model for saving thoughts tied to a book (and a user)
class Note(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    chapter = db.Column(db.Integer, nullable=True)
    page = db.Column(db.Integer, nullable=True)
    content = db.Column(db.Text, nullable=False)
    book_id = db.Column(db.Integer, db.ForeignKey('book.id'), nullable = False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
