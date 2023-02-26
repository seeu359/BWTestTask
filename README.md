[![code-check](https://github.com/seeu359/BWTestTask/actions/workflows/linter_and_tests_check.yaml/badge.svg)](https://github.com/seeu359/BWTestTask/actions/workflows/linter_and_tests_check.yaml)

---

### Installation

1. Clone repo: $ git clone https://github.com/seeu359/BWTestTask.git

2. Go to the directory with code

#### If you use docker:

1. Use `$ make build` command to create two docker containers: with app and with postgres
2. Use `$ make migration` to create alembic migrations
3. Use `$ make head` to apply migrations
4. Go to http://0.0.0.0:8000

Use `$ make rm` to delete containers and app image.

#### Else

1. Set the dependencies:
2. If you're using poetry, run command: ``$ make p_install``
3. Else: `$ make install`


#### Environment variables


Example file with environment variables - .env.example

----

Set the migrations by alembic