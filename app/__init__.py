from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_mail import Message, Mail
from redis import Redis
import os

db = SQLAlchemy()
r = Redis(host="localhost", port=6379, db=0)
mail = Mail()

def create_app():
    app = Flask(__name__)
    db.init_app(app) 
    mail.init_app(app)
    
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///db.sqlite3"
    app.config["DEBUG"] = True
    app.config["MAIL_SERVER"] = "smtp.gmail.com"
    app.config["MAIL_PORT"] = 587
    app.config["MAIL_USE_TLS"] = True
    app.config["MAIL_USE_SSL"] = False
    app.config["MAIL_USERNAME"] = "paschal.uwakwe.247760@unn.edu.ng"
    app.config["MAIL_PASSWORD"] = os.environ.get("EMAIL_PASSWORD")
    app.config["MAIL_DEFAULT_SENDER"] = "paschal.uwakwe.247760@unn.edu.ng"
    app.config["MAIL_MAX_EMAILS"] = 5
    # app.config["MAIL_SUPRESS_SEND"] = False
    # app.config["MAIL_ASCII_ATTACHMENTS"] = False
    print(os.environ.get("EMAIL_PASSWORD"))

    from .v1 import blueprint as v1

    app.register_blueprint(v1)

    return app