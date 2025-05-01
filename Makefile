
format:
	./env/bin/black .
	./env/bin/isort .
	./env/bin/flake8 .
#	./env/bin/mypy .

test:
	python -m pytest
