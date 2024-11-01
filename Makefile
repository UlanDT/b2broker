install:
	poetry env use python3.11
	poetry config virtualenvs.create true
	poetry config virtualenvs.in-project true
	poetry install

install-deploy:
	poetry config virtualenvs.create false
	poetry install --only main --no-root --no-cache

lint:
	mypy .
	ruff format --check  .
	black --check .

format:
	ruff format .
	ruff check --fix --exit-zero --silent
	black .

test:
	coverage run -m pytest
	coverage html

setup:
	cp .env.example .env
	docker compose up -d --build
