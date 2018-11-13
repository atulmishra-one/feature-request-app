from app.main import create_request_app
from app import config

application = create_request_app(config)
if __name__ == '__main__':
    application.run()
