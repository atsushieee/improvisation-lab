.PHONY: install
install:
	poetry install

.PHONY: run
run:
	poetry run python main.py

.PHONY: lint
lint:
	poetry run pflake8 improvisation_lab tests
	poetry run mypy improvisation_lab tests
	poetry run pydocstyle improvisation_lab tests

.PHONY: format
format:
	poetry run black improvisation_lab tests
	poetry run isort improvisation_lab tests

.PHONY: test
test:
	poetry run pytest -vs tests
