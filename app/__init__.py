from flask import Flask
from flask_cors import CORS
from flasgger import Swagger

from app.api.v1 import auth_blueprint, app_blueprint
from instance.config import APP_CONFIG


def create_app(config_setting):
    app = Flask(__name__)
    app.register_blueprint(auth_blueprint)
    app.register_blueprint(app_blueprint)

    app.config.from_object(
        APP_CONFIG[config_setting.strip().lower()])

    CORS(app)

    description = "Questioner is an API application allowing a user to\
                    register, login, ask questions to meetups and\
                    vote on questions posted to present meetups."

    template = {
        "swagger": "3.0",
        "info": {
            "title": "Questioner API",
            "description": description,
            "version": "1.0"
        }
    }

    Swagger(app, template=template)

    return app
