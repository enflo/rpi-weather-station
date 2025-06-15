
format:
	./env/bin/ruff check .
	./env/bin/ruff format .
#	./env/bin/mypy .

test:
	python -m pytest
