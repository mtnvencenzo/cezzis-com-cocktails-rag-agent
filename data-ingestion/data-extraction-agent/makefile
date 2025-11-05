.PHONY: install run test py-source

install:
	pip install -r requirements.txt -r requirements-dev.txt

py-source:
	. .venv/bin/activate && \
	export PATH=".venv/bin::PATH" && \
	exec "$$SHELL"

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