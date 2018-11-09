from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
DEBUG = True
SECRET_KEY = r'1\xc4ss\xcd;\xc4cC\x01\xf7\x8d\xfe,'
SQLALCHEMY_DATABASE_URI = "sqlite:///{0}".format(Path(BASE_DIR).joinpath('app.db'))
