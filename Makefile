

# Development
docker-build-dev:
	docker-compose -f docker-compose-dev.yml build

docker-up-dev:
	docker-compose -f docker-compose-dev.yml up

docker-up-dev-background:
	docker-compose -f docker-compose-dev.yml up -d

docker-build-up-dev:
	docker-compose -f docker-compose-dev.yml up --build -d

# Production
docker-build:
	docker-compose -f docker-compose-prod.yml build

docker-up:
	docker-compose -f docker-compose-prod.yml up

docker-up-background:
	docker-compose -f docker-compose-prod.yml up -d

docker-build-up:
	docker-compose -f docker-compose.yml up --build -d

# Testing
docker-test-functional:
	docker exec -it django python3 manage.py test functional_tests

docker-test-unit:
	docker exec -it django python3 manage.py test lists

docker-migration:
	docker exec -it django python3 manage.py makemigrations

docker-migrate:
	docker exec -it django python3 manage.py migrate --run-syncdb
