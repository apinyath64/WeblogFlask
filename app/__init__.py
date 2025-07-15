from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from os import path
from flask_login import LoginManager
import os
from dotenv import load_dotenv

load_dotenv()
db = SQLAlchemy()
DB_NAME = "weblog.db"

def create_app():
    app = Flask(__name__)
    app.secret_key = "my_secret_123"
    app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get('DATABASE_URL', f'sqlite:///{DB_NAME}')
    # initialize database
    db.init_app(app)

    from .views import views
    from .auth import auth

    app.register_blueprint(views, url_prefix="/")
    app.register_blueprint(auth, url_prefix="/")

    from .models import User, Post, Comment
    # create_database(app)
    with app.app_context():
        db.create_all()
        print("Create database successfully!")


    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(id):
        return User.query.get(int(id))

    return app


def create_database(app):
    # if database not exits create it
    if not path.exists('app/' + DB_NAME):
        db.create_all(app=app)
        print("Create Database Successfully!")
