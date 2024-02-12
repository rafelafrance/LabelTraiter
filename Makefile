.PHONY: test install dev venv clean
.ONESHELL:

VENV=.venv
PY_VER=python3.11
PYTHON=./$(VENV)/bin/$(PY_VER)
PIP_INSTALL=$(PYTHON) -m pip install
SPACY_MODEL=$(PYTHON) -m spacy download en_core_web_md

test:
	$(PYTHON) -m unittest discover

install: venv
	source $(VENV)/bin/activate
	$(PIP_INSTALL) -U pip setuptools wheel
	$(PIP_INSTALL) git+https://github.com/rafelafrance/common_utils.git@main#egg=common_utils
	$(PIP_INSTALL) git+https://github.com/rafelafrance/traiter.git@master#egg=traiter
	$(PIP_INSTALL) git+https://github.com/rafelafrance/FloraTraiter.git@main#egg=FloraTraiter
	$(PIP_INSTALL) .
	$(SPACY_MODEL)

dev: venv
	source $(VENV)/bin/activate
	$(PIP_INSTALL) -U pip setuptools wheel
	$(PIP_INSTALL) -e ../../misc/common_utils
	$(PIP_INSTALL) -e ../../traiter/traiter
	$(PIP_INSTALL) -e ../../traiter/FloraTraiter
	$(PIP_INSTALL) -e .[dev]
	$(SPACY_MODEL)
	pre-commit install

venv:
	test -d $(VENV) || $(PY_VER) -m venv $(VENV)

clean:
	rm -r $(VENV)
	find -iname "*.pyc" -delete
