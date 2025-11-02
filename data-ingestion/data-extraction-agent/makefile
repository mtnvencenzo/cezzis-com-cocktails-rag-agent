.PHONY: install run test

install:
	pip install -r requirements.txt -r requirements-dev.txt

py-source:
	source .venv/bin/activate

run:
	cd src && ENV="local" python3 app.py

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