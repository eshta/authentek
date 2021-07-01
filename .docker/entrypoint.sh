#!/bin/bash

export FLASK_APP=authentek/app.py
export APP_SETTINGS="authentek.server.config.DevelopmentConfig"
set -e

export PYTHONPATH=.:$PYTHONPATH


#pip install -e .
#python manage.py create_db
#python manage.py db init
#python manage.py db migrate
#flask db upgrade

RETRIES=10

until psql -h $PG_HOST -U $PG_USER -d $PG_DATABASE -c "select 1" > /dev/null 2>&1 || [ $RETRIES -eq 0 ]; do
  echo "Waiting for postgres server to start, $((RETRIES)) remaining attempts..."   RETRIES=$((RETRIES-=1))
  sleep 1
done

# gunicorn -c gunicorn.config.py wsgi:app
make run
