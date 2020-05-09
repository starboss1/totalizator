import os
from dotenv import load_dotenv

load_dotenv()


class Config(object):
    DEBUG = False
    CSRF_ENABLED = True
    PORT = 8000
    HOST = "localhost"
    LOG_TO_STDOUT = os.environ.get('LOG_TO_STDOUT')
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-will-never-guess'

    DB_NAME = os.getenv('DB_NAME')
    DB_PORT = os.getenv('DB_PORT')
    DB_HOST = os.getenv('DB_HOST')
    DB_PASS = os.getenv('DB_PASS')
    DB_USER = os.getenv('DB_USER')

    SQLALCHEMY_DATABASE_URI = f"postgresql://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
    #SQLALCHEMY_DATABASE_URI = os.environ.get("DATABASE_URL")
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    USER_ENABLE_EMAIL = False
    USER_ENABLE_USERNAME = True

    USER_PASSLIB_CRYPTCONTEXT_SCHEMES = ["sha256_crypt"]

    USER_ENABLE_CONFIRM_EMAIL = False

    USER_LOGIN_TEMPLATE = 'authentication/login.html'
    USER_REGISTER_TEMPLATE = 'authentication/register.html'


class ProductionConfig(Config):
    PORT = 80
    HOST = "0.0.0.0"
    DEBUG = False


class DevelopmentConfig(Config):
    DEVELOPMENT = True
    DEBUG = True


config_object = DevelopmentConfig()
