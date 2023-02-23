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