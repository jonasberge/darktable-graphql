#!make
include .env
export

VENV_DIR=venv
VENV_ACTIVATE=$(VENV_DIR)/bin/activate
ORM_GEN_DIR=src/dtgraphql/gen

./$(VENV_DIR):
	python3 -m venv $(VENV_DIR)
	. $(VENV_ACTIVATE); \
		python3 -m pip install pip --upgrade; \
		python3 -m pip install -r requirements.txt

pip-freeze: ./$(VENV_DIR)
	. $(VENV_ACTIVATE); \
		pip freeze | tee requirements.txt
