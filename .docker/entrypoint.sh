#!/bin/sh

export FLASK_APP=authentek/app.py
export APP_SETTINGS="authentek.server.config.DevelopmentConfig"
#export SECRET_KEY="\x04:\xe7\x17*\x0f\xcf\xa5=\x0b\xd8H8_\x8d\x14\xa6\x98w\xa9{\x15\x84$"
#export PG_URI="postgresql://test:test@postgres:5432/"
set -e

export PYTHONPATH=.:$PYTHONPATH


#pip install -e .
#python manage.py create_db
#python manage.py db init
#python manage.py db migrate
#flask db upgrade

RETRIES=10

until psql -h $PG_HOST -U $PG_USER -d $PG_DATABASE -c "select 1" > /dev/null 2>&1 || [ $RETRIES -eq 0 ]; do
  echo "Waiting for postgres server, $((RETRIES--)) remaining attempts..."
  sleep 1
done

# gunicorn -c gunicorn.config.py wsgi:app
make run
