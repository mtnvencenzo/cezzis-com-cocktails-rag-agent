.PHONY: install run

install:
	pip install -r requirements.txt

run:
	cd src && ENV="local" python3 app.py

api-client:
	cd src && \
	openapi-python-client generate \
		--url "https://api.cezzis.com/prd/cocktails/api-docs/v1/scalar/v1/openapi.json" \
		--output-path ./cocktails_api \
		--config ./cocktails_api/cocktails_api.yaml \
		--overwrite