.PHONY: venv
venv:
	poetry install --no-root

.PHONY: format
format:
	poetry run ruff format

.PHONY: check
check:
	poetry run ruff check

.PHONY: run
run:
    poetry run python3 -m codexrunarum
