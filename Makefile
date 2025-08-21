VENV_DIR = venv
PYTHON = python3.13
PIP = $(VENV_DIR)/bin/pip
PYTHON_VENV = $(VENV_DIR)/bin/python
PRE_COMMIT = $(VENV_DIR)/bin/pre-commit
PKG_NAME = schema_first
SRC_DIR = src/$(PKG_NAME)

.PHONY: venv test format clean build install upload_to_testpypi upload_to_pypi all

venv: venv/pyvenv.cfg $(PKG_DIR)
	# Create virtual environment.

venv/pyvenv.cfg: pyproject.toml $(PKG_DIR)
	$(PYTHON) -m venv $(VENV_DIR)
	$(PIP) -q install --upgrade pip wheel
	$(PIP) -q install -e ".[dev]" && $(PIP) -q install -e .

format: venv
	# Run checking and formatting sources.
	$(PRE_COMMIT) run -a

test: venv
	# Run pytest.
	./venv/bin/bandit -q -r src/
	./venv/bin/pytest -s -x --cov-report term-missing:skip-covered --cov=$(SRC_DIR) tests/

clean:
	rm -rf venv/
	rm -rf dist/
	rm -rf src/Schema_First.egg-info

build: clean venv
	$(PYTHON_VENV) -m build

install: clean venv build
	$(PIP) install dist/$(PKG_NAME)-*.tar.gz
	pre-commit install

upload_to_testpypi: build
	$(PYTHON_VENV) -m twine upload --repository testpypi dist/*

upload_to_pypi: build
	$(PYTHON_VENV) -m twine upload --repository pypi dist/*

all: install test
