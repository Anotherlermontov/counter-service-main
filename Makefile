DOCKER_COMPOSE_FILE = docker-compose.yml

lock:
	pip-compile --generate-hashes --no-emit-index-url --allow-unsafe
	pip-compile --generate-hashes --no-emit-index-url requirements_dev.in

install-dev:
	pip-sync requirements.txt requirements_dev.txt --pip-args '--no-deps'

migrate:
	docker exec main-service ./manage.py migrate --noinput

build:
	docker compose -f ${DOCKER_COMPOSE_FILE} build

up:
	docker compose -f ${DOCKER_COMPOSE_FILE} up

up-d:
	docker compose -f ${DOCKER_COMPOSE_FILE} up -d

up_db:
	docker compose -f ${DOCKER_COMPOSE_FILE} up counter-service-db

up_db-d:
	docker compose -f ${DOCKER_COMPOSE_FILE} up counter-service-db -d

log:
	docker compose -f ${DOCKER_COMPOSE_FILE} logs -f --tail 100

stop:
	docker compose -f ${DOCKER_COMPOSE_FILE} stop

down:
	docker compose -f ${DOCKER_COMPOSE_FILE} down
