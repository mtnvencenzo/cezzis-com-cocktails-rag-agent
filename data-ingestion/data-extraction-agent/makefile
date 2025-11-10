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

models:
	poetry run datamodel-codegen --url "https://api.cezzis.com/prd/cocktails/api-docs/v1/scalar/v1/openapi.json" --input-file-type openapi --output src/cocktail_models.py --output-model-type pydantic_v2.BaseModel --field-constraints --use-default --use-schema-description --target-python-version 3.12

coverage:
	poetry run pytest -v --cov=src --cov-report=xml:coverage.xml --cov-report=term --junitxml=pytest-results.xml

standards:
	@make ruff-check
	@echo "Code standards check complete."
	@make ruff-format
	@echo "Code formatting complete."