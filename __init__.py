from flask import Flask, Blueprint, current_app

from .views import main


def create_app(config_file='settings.py'):
    app = Flask(__name__)
    
    app.config.from_pyfile(config_file)
    app.register_blueprint(main)

    return app