from flask import Flask, Blueprint, current_app
# from flask_login import login_required, UserMixin, LoginManager, login_user, logout_user, current_user
from db import mysql

from .views import main
from record import record
# login_manager = LoginManager()
# login_manager.login_view = 'login'
# login_manager.init_app(main)

# @login_manager.user_loader
# def load_user(user_id):
#     return User.query.get(int(user_id))

def create_app(config_file='settings.py'):
    app = Flask(__name__)
    app.config['MYSQL_HOST'] = 'localhost'
    app.config['MYSQL_USER'] = 'root'
    app.config['MYSQL_PASSWORD'] = 'password'
    app.config['MYSQL_DB'] = 'hospital_dbms'
    mysql.init_app(app)
    app.config.from_pyfile(config_file)
    app.register_blueprint(main)
    app.register_blueprint(record)
    return app