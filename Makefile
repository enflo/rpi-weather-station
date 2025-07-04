
format:
	./env/bin/ruff check .
	./env/bin/ruff format .

test:
	python -m pytest
