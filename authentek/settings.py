import os

# Flask settings
FLASK_SERVER_NAME = '0.0.0.0:8888'
FLASK_DEBUG = True  # Do not use debug mode in production
ENV = os.getenv('STAGE', 'dev')

# Flask-Restplus settings
RESTPLUS_SWAGGER_UI_DOC_EXPANSION = 'list'
RESTPLUS_VALIDATE = True
RESTPLUS_MASK_SWAGGER = False
RESTPLUS_ERROR_404_HELP = False

basedir = os.path.abspath(os.path.dirname(__file__))
postgres_local_base = os.getenv('PG_URI', 'postgresql://postgres:postgres@postgres/')
database_name = 'auth'

BCRYPT_LOG_ROUNDS = 13
SQLALCHEMY_TRACK_MODIFICATIONS = False
SECRET_KEY = os.getenv('SECRET_KEY', 'my_precious')
JWT_TTL = int(os.getenv('JWT_TTL', '5'))
SQLALCHEMY_DATABASE_URI = postgres_local_base + database_name
