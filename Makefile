#   python3 -m venv .venv
#   .venv/bin/pip install -r requirements.txt -r dev_requirements.txt
#   source .venv/bin/activate
#   make test

PYTHON ?= python

.PHONY: test unit_test perf_test coverage lint doc

test:
	$(PYTHON) -m pytest

unit_test:
	$(PYTHON) -m pytest -m "not performance"

perf_test:
	$(PYTHON) -m pytest -m performance

coverage:
	-$(PYTHON) -m coverage run -m pytest -m "not performance"
	$(PYTHON) -m coverage report -m
	$(PYTHON) -m coverage html

lint:
	$(PYTHON) -m ruff check .

doc:
	rm -rf docs/triangulator
	$(PYTHON) -m pdoc --html -o docs triangulator
