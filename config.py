import os
from dotenv import load_dotenv

load_dotenv()


class Config(object):
    DEBUG = False
    CSRF_ENABLED = True
    PORT = 8000
    HOST = "localhost"


class ProductionConfig(Config):
    PORT = 80
    HOST = "0.0.0.0"
    DEBUG = False


class DevelopmentConfig(Config):
    DEVELOPMENT = True
    DEBUG = True


config_object = DevelopmentConfig()
