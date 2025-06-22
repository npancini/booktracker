from app.models import db, User, Book, Note

def register(client, username="testuser", password="testpass"):
    return client.post('/register', data={
        'username': username,
        'password': password
    }, follow_redirects=True)

def login(client, username="testuser", password="testpass"):
    return client.post('/login', data={
        'username': username,
        'password': password
    }, follow_redirects=True)

def test_register_and_login(client):
    # Register user
    res = register(client)
    assert b'Login' in res.data

    # Login user
    res = login(client)
    assert b'<table' in res.data

def test_home_requires_login(client):
    res = client.get('/home')
    # should redirect to login
    assert res.status_code == 302
    assert '/login' in res.headers['Location']

def test_add_book(client, app):
    register(client)
    login(client)

    res = client.post('/addb', data={
        'title': 'Test Book',
        'author': 'Author Name'
    }, follow_redirects=True)

    assert b'Test Book' in res.data

def test_book_details(client, app):
    register(client)
    login(client)

    # Add book
    client.post('/addb', data={'title': '1984', 'author': 'George Orwell'}, follow_redirects=True)
    book = Book.query.first()

    res = client.get(f'/book/{book.id}')
    assert b'1984' in res.data

def test_add_note(client, app):
    register(client)
    login(client)

    # Add book
    client.post('/addb', data={'title': 'Book w/ Note', 'author': 'A'}, follow_redirects=True)
    book = Book.query.first()

    # Add note to book
    res = client.post(f'/book/{book.id}', data={
        'form_id': 'note',
        'chapter': '1',
        'page': '5',
        'content': 'Interesting part'
    }, follow_redirects=True)

    assert b'Interesting part' in res.data

def test_mark_as_finished_and_current(client, app):
    register(client)
    login(client)

    client.post('/addb', data={'title': 'Finish Me', 'author': 'A'}, follow_redirects=True)
    book = Book.query.first()

    # Mark as finished
    res = client.post(f'/book/{book.id}/finish', follow_redirects=True)
    assert b'Finish Me' in res.data
    book = Book.query.get(book.id)
    assert book.finished is True
    assert book.finish_date is not None

    # Mark as current again
    res = client.post(f'/book/{book.id}/current', follow_redirects=True)
    book = Book.query.get(book.id)
    assert book.finished is False
    assert book.finish_date is None

def test_delete_book_and_note(client, app):
    register(client)
    login(client)

    # Add book and note
    client.post('/addb', data={'title': 'Temp Book', 'author': 'A'}, follow_redirects=True)
    book = Book.query.first()
    client.post(f'/book/{book.id}', data={
        'form_id': 'note',
        'chapter': '',
        'page': '',
        'content': 'To be deleted'
    }, follow_redirects=True)
    note = Note.query.first()

    # Delete note
    res = client.get(f'/deleten/{note.id}', follow_redirects=True)
    assert b'To be deleted' not in res.data

    # Delete book
    res = client.get(f'/deleteb/{book.id}', follow_redirects=True)
    assert b'Temp Book' not in res.data
