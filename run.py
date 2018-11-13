from app.main import create_request_app as application
from app import config

if __name__ == '__main__':
    application = application(config)
    application.run()
