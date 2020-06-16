# use the rest as arguments for targets
TARGET_ARGS := $(wordlist 2,$(words $(MAKECMDGOALS)),$(MAKECMDGOALS))
# ...and turn them into do-nothing targets
$(eval $(TARGET_ARGS):;@:)

start:
	docker-compose up -d

run: install
	python authentek/app.py
	#gunicorn -c gunicorn.config.py wsgi:app

run-prod: install
	gunicorn -c gunicorn.config.py wsgi:app

install:
	python manage.py create_db
	python manage.py init
	python manage.py migrate
	#python setup.py develop

test:
	STAGE=test APP_SETTINGS="authentek.server.config.TestingConfig" pytest

run-testcase:
	STAGE=test APP_SETTINGS="authentek.server.config.TestingConfig" pytest -k $(TARGET_ARGS)

freeze:
	pipenv run pipenv_to_requirements

clean:
	docker-compose stop; docker-compose rm -svf

restart:
	docker-compose restart $(TsARGET_ARGS)

clean-restart:
	docker-compose stop $(TARGET_ARGS) && docker-compose rm -f $(TARGET_ARGS) && make rebuild $(TARGET_ARGS) && docker-compose -f docker-compose.yml up -d

soft-restart:
	docker-compose stop $(TARGET_ARGS) && docker-compose rm -f $(TARGET_ARGS) && docker-compose -f docker-compose.yml up -d

clean-pg:
	rm -rf .docker/data/pg/*
	make clean-restart postgres && make logs postgres

rebuild:
	docker-compose build --force-rm $(TARGET_ARGS)
bash:
	docker-compose exec $(TARGET_ARGS) bash

logs:
	docker-compose logs -f $(TARGET_ARGS)
