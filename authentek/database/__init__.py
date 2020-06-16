from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


def reset_database():
    from authentek.database.models import User, BlacklistToken  # noqa
    db.drop_all()
    db.create_all()
