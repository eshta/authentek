# project/server/config.py

import os
basedir = os.path.abspath(os.path.dirname(__file__))
postgres_local_base = os.getenv('PG_URI', 'postgresql://postgres:postgres@postgres/')
database_name = 'auth'


class BaseConfig:
    """Base configuration."""
    DEBUG = False
    BCRYPT_LOG_ROUNDS = 13
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = os.getenv('SECRET_KEY', 'my_precious')
    JWT_TTL = 2592000
    SQLALCHEMY_DATABASE_URI = postgres_local_base + database_name

    MAIL_SERVER = os.getenv('MAIL_SERVER', 'smtp.gmail.com')
    MAIL_PORT = 465
    MAIL_USERNAME = os.getenv('MAIL_USERNAME', '')
    MAIL_PASSWORD = os.getenv('MAIL_PASSWORD', '')
    MAIL_USE_TLS = False
    MAIL_USE_SSL = True

class DevelopmentConfig(BaseConfig):
    """Development configuration."""
    DEBUG = True
    BCRYPT_LOG_ROUNDS = 4

class TestingConfig(BaseConfig):
    """Testing configuration."""
    DEBUG = False
    TESTING = True
    BCRYPT_LOG_ROUNDS = 4
    SQLALCHEMY_DATABASE_URI = postgres_local_base + database_name + '_test'
    PRESERVE_CONTEXT_ON_EXCEPTION = False


class ProductionConfig(BaseConfig):
    """Production configuration."""
    SECRET_KEY = os.getenv('SECRET_KEY', 'my_precious')

    DEBUG = False
