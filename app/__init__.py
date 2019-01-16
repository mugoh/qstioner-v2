from flask import Flask
from flask_cors import CORS
from flasgger import Swagger

from app.api.v2 import auth_blueprint, app_blueprint
from instance.config import APP_CONFIG
from app.api.v2.database.database import db_instance


def create_app(config_setting):
    app = Flask(__name__)
    app.register_blueprint(auth_blueprint)
    app.register_blueprint(app_blueprint)

    app.config.from_object(
        APP_CONFIG[config_setting.strip().lower()])

    CORS(app)

    db_instance.drop_tables()
    db_instance.create_tables()

    description = "Questioner is an API application allowing a user to\
                    register, login, ask questions to meetups and\
                    vote on questions posted to present meetups."

    template = {
        "swagger": "3.0",
        "info": {
            "title": "Questioner API",
            "description": description,
            "version": "2.0"
        }
    }

    Swagger(app, template=template)

    return app
