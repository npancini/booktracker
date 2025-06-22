from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from .models import db, User

login_manager = LoginManager()
login_manager.login_view = 'routes.login'

def create_app(config=None):
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'dev'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///books.db'

    if config:
        app.config.update(config)

    db.init_app(app)
    login_manager.init_app(app)

    from .routes import routes
    app.register_blueprint(routes)

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    with app.app_context():
        db.create_all()

    return app
