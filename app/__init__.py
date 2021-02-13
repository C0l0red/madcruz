from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from redis import Redis

db = SQLAlchemy()
r = Redis(host="localhost", port=6379, db=0)

def create_app():
    app = Flask(__name__)
    db.init_app(app) 
    
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///db.sqlite3"

    from .v1 import api as v1

    app.register_blueprint(v1)

    return app