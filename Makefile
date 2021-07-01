# use the rest as arguments for targets
TARGET_ARGS := $(wordlist 2,$(words $(MAKECMDGOALS)),$(MAKECMDGOALS))
# ...and turn them into do-nothing targets
$(eval $(TARGET_ARGS):;@:)

-include .env

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

tox:
	docker-compose run -v $(PWD)/tests:/code/tests:ro web tox -e py37

lint:
	docker-compose run auth tox -e lint

start:
	docker-compose up -d

logs:
	docker-compose logs -f --tail=100 $(TARGET_ARGS)

bash:
	docker-compose exec $(TARGET_ARGS) bash

rebuild:
	docker-compose build --force-rm $(TARGET_ARGS)

clean-restart:
	docker-compose stop $(TARGET_ARGS) && docker-compose rm -f $(TARGET_ARGS) && make rebuild $(TARGET_ARGS) && docker-compose up -d --no-deps --build $(TARGET_ARGS)

soft-restart:
	docker-compose stop $(TARGET_ARGS) && docker-compose rm -f $(TARGET_ARGS) && docker-compose up -d


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
