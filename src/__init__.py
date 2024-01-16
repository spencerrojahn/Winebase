import os
from flask import Flask, Blueprint
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

MYSQL_USER = os.environ.get('MYSQL_WINEBASE_USER')
MYSQL_PASSWORD = os.environ.get('MYSQL_WINEBASE_PASSWORD')
MYSQL_SERVER_HOST = 'localhost'
MYSQL_DB_NAME = 'Winebase'

db = SQLAlchemy()

from .models import User
from .blueprints.tabs import base_bp, tabs
from .blueprints.auth import auth
from .blueprints.apis.wines import wines
from .blueprints.apis.cellars import cellars
from .blueprints.apis.owners import owners



def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'blah blah'
    app.config['SQLALCHEMY_DATABASE_URI'] = f'mysql+pymysql://{MYSQL_USER}:{MYSQL_PASSWORD}@{MYSQL_SERVER_HOST}/{MYSQL_DB_NAME}'
    db.init_app(app)

    app.register_blueprint(base_bp, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/auth/')
    app.register_blueprint(wines, url_prefix='/api/wines/')
    app.register_blueprint(cellars, url_prefix='/api/cellars/')
    app.register_blueprint(owners, url_prefix='/api/owners/')
    app.register_blueprint(tabs, url_prefix='/tabs/')
    

    with app.app_context():
        db.create_all()

    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(id):
        return User.query.get(int(id))

    return app