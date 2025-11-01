.PHONY: install run test

install:
	pip install -r requirements.txt -r requirements-dev.txt

run:
	cd src && ENV="local" python3 app.py

api-client:
	cd src && \
	openapi-python-client generate \
		--url "https://api.cezzis.com/prd/cocktails/api-docs/v1/scalar/v1/openapi.json" \
		--output-path ./cocktails_api \
		--config ./cocktails_api/cocktails_api.yaml \
		--overwrite

ruff-check:
	ruff check --fix . --config .ruff.toml

ruff-format:
	ruff format . --config .ruff.toml

test:
	pytest test/

standards:
	@make ruff-check
	@echo "Code standards check complete."
	@make ruff-format
	@echo "Code formatting complete."