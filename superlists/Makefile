
docker-build:
	docker-compose build


docker-up:
	docker-compose up -d

docker-test-functional:
	docker exec -it django python3 manage.py test functional_tests

docker-test-unit:
	docker exec -it django python3 manage.py test lists

docker-migration:
	docker exec -it django python3 manage.py makemigrations
