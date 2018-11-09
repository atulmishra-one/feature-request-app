from flask import Flask
from app.extensions import db
from app.views import app_views


def create_request_app(settings):
    """"Creates the application factory.

    `The Feature request app` registers the below extensions:
    SqlAlchemy with sqlite db
    """
    application = Flask(__name__)
    application.config.from_object(settings)

    db.init_app(application)

    application.register_blueprint(app_views)
    return application

