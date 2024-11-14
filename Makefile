.PHONY: install
install:
	poetry install

.PHONY: run
run:
	poetry run python main.py

.PHONY: lint
lint:
	poetry run pflake8 improvisation_lab tests main.py
	poetry run mypy improvisation_lab tests main.py
	poetry run pydocstyle improvisation_lab tests main.py

.PHONY: format
format:
	poetry run black improvisation_lab tests main.py
	poetry run isort improvisation_lab tests main.py

.PHONY: test
test:
	poetry run pytest -vs tests

.PHONY: pitch-demo
pitch-demo:
	poetry run python scripts/pitch_detection_demo.py
