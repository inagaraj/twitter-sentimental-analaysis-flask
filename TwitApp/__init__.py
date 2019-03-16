from flask import Flask
from flask_sqlalchemy import SQLAlchemy

from TwitApp.config import Config

db = SQLAlchemy()


def create_app(config_class=Config):
    app = Flask(__name__)
   

   

    from TwitApp.routes import tweet
    app.register_blueprint(tweet)

  

    return app
