.PHONY: install
install:
	poetry install

.PHONY: run
run:
	poetry run python main.py

.PHONY: lint
lint:
	poetry run pflake8 improvisation_lab scripts tests main.py
	poetry run mypy improvisation_lab scripts tests main.py
	poetry run pydocstyle improvisation_lab scripts tests main.py

.PHONY: format
format:
	poetry run black improvisation_lab scripts tests main.py
	poetry run isort improvisation_lab scripts tests main.py

.PHONY: test
test:
	poetry run pytest -vs tests

.PHONY: pitch-demo-web pitch-demo-direct
pitch-demo-web:
	poetry run python scripts/pitch_detection_demo.py --input web

pitch-demo-direct:
	poetry run python scripts/pitch_detection_demo.py --input direct

# Target alias (Default: input voice via web)
.PHONY: pitch-demo
pitch-demo: pitch-demo-web
