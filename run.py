from app.main import create_request_app
from app import config

if __name__ == '__main__':
    app = create_request_app(config)
    app.run()
