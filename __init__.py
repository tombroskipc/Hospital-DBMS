from flask import Flask, Blueprint

from .views import main

def create_app():
    app = Flask(__name__)
    

    # @main.route('/')
    # def index():
    #     return '<h1>Hello World!</h1>'

    app.register_blueprint(main)

    return app