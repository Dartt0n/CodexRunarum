.PHONY: venv
venv:
	poetry install --no-root

.PHONY: format
format:
	poetry run ruff format

.PHONY: check
check:
	poetry run ruff check
