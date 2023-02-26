run:
	poetry run python3 main.py

p_install:
	poetry install

install:
	pip install -r requirements.txt

sort:
	poetry run isort .

lint:
	poetry run flake8

test:
	poetry run pytest tests

build:
	docker-compose up -d

migration:
	docker exec api alembic revision --autogenerate

head:
	docker exec api alembic upgrade head


rm:
	docker stop api
	docker stop postgres_db
	docker rm api
	docker rm postgres_db
	docker rmi bwtesttask-server