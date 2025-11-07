.PHONY: install build test shell ruff-check ruff-format coverage standards

install:
	poetry install --no-root

shell:
	poetry shell

ruff-check:
	poetry run ruff check --fix . --config .ruff.toml

ruff-format:
	poetry run ruff format . --config .ruff.toml

test:
	poetry run pytest test/

coverage:
	poetry run pytest -v --cov=src --cov-report=xml:coverage.xml --cov-report=term --junitxml=pytest-results.xml

standards:
	@make ruff-check
	@echo "Code standards check complete."
	@make ruff-format
	@echo "Code formatting complete."