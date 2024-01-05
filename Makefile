VENV=.venv
PYTHON=$(VENV)/bin/python3
# DATABASE_URL := $(shell python3 _get_database_url.py)

venv:
	python3 -m venv $(VENV)
	@echo 'Path to Python executable $(shell pwd)/$(PYTHON)'

pre_commit_install:
	@echo "=== Installing pre-commit ==="
	$(PYTHON) -m pre_commit install

install_all: venv
	@echo "=== Installing common dependencies ==="
	$(PYTHON) -m pip install -r requirements.txt

	make pre_commit_install
