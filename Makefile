.PHONY: init init-migration build run db-migrate test tox

init:  build run
	docker-compose exec web authentek db upgrade
	docker-compose exec web authentek init
	@echo "Init done, containers running"

build:
	docker-compose build

run:
	docker-compose up -d

db-migrate:
	docker-compose exec web authentek db migrate

db-upgrade:
	docker-compose exec web authentek db upgrade

test:
	docker-compose run -v $(PWD)/tests:/code/tests:ro web tox -e test

tox:
	docker-compose run -v $(PWD)/tests:/code/tests:ro web tox -e py37

lint:
	docker-compose run web tox -e lint

start:
	docker-compose up -d


run: install
	python authentek/app.py
	gunicorn -c gunicorn.config.py authentek.wsgi:app --access-logfile '-' --error-logfile '-'

run-prod: install
	gunicorn -c gunicorn.config.py wsgi:app

install:
	pip install -e .
# 	authentek db init
	authentek db upgrade head
	#python setup.py develop

test:
	STAGE=test APP_SETTINGS="authentek.server.config.TestingConfig" pytest

freeze:
	pipenv run pipenv_to_requirements
