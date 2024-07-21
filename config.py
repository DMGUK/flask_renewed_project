import os
from datetime import timedelta

from dotenv import load_dotenv

load_dotenv('migrations/database_link.env')
app_root_path = os.path.dirname(os.path.abspath(__file__))


class Config:
    SECRET_KEY = b"secretkey"
    WTF_CSRF_ENABLED = True
    SQLALCHEMY_TRACK_MODIFICATIONS = False

class DevelopmentConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = f'{os.getenv("DB_URL")}'

class ProductionConfig(Config):
    DEBUG = False
    SQLALCHEMY_DATABASE_URI = f'{os.getenv("DB_URL")}'

class TestingConfig(Config):
    TESTING = True
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'
    WTF_CSRF_ENABLED = False
