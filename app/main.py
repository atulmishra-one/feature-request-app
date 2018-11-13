import logging
from logging.handlers import RotatingFileHandler

from flask import Flask
from app.extensions import db
from app.views import app_views
from app.api import api_views


def create_request_app(settings):
    """"Creates the application factory.

    `The Feature request app` registers the below extensions:
    SqlAlchemy with sqlite db
    """
    application = Flask(__name__)
    application.config.from_object(settings)

    db.init_app(application)

    application.register_blueprint(app_views)
    application.register_blueprint(api_views)

    logging_handler = RotatingFileHandler("{0}/app.log".format(settings.BASE_DIR), maxBytes=10000, backupCount=1)
    logging_handler.setLevel(logging.INFO)
    application.logger.addHandler(logging_handler)
    with application.app_context():
        db.create_all()
    return application

