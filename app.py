from flask import Flask
from flask_smorest import Api

from resources.item import blp as ItemBlueprint
from resources.store import blp as StoreBlueprint
from resources.health import blp as HealthBluePrint
from resources.users import blp as UserBlueprint

from dotenv import load_dotenv
import os
from db import db
import models

import redis
from rq import Queue

def create_app(db_url = None):
    app = Flask(__name__)
    load_dotenv()

    connection = redis.from_url(os.getenv("REDIS_URL"))
    app.queue = Queue("emails", connection=connection)
    app.config["PROPAGATE_EXCEPTIONS"] = True
    app.config["API_TITLE"] = "Stores REST API"
    app.config["API_VERSION"] = "v1"
    app.config["OPENAPI_VERSION"] = "3.0.3"
    app.config["OPENAPI_URL_PREFIX"] = "/"
    app.config["OPENAPI_SWAGGER_UI_PATH"] = "/swagger-ui"
    app.config["OPENAPI_SWAGGER_UI_URL"] = "https://cdn.jsdelivr.net/npm/swagger-ui-dist/"
    app.config["SQLALCHEMY_DATABASE_URI"] = db_url or os.getenv("DATABASE_URL", "sqlite:///data.db") # use db_url argument if passed, else use database_url from environment variables or default to sqlite url
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    db.init_app(app) # initializes flask-sqlalchemy extension

    api = Api(app)

    # Manually create an application context
    with app.app_context():
    # Now you have access to the application context
    # Perform actions that require the application context here
        db.create_all()  # This will create the database tables if they don't exist already

    api.register_blueprint(ItemBlueprint)
    api.register_blueprint(StoreBlueprint)
    api.register_blueprint(HealthBluePrint)
    api.register_blueprint(UserBlueprint)

    return app

app = create_app()
