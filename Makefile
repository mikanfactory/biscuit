BASE_PYTHON := $(shell which python3)
PIPENV      := $(shell which pipenv)
PYTHON      := .venv/bin/python
PIP         := .venv/bin/pip
PYTEST      := .venv/bin/pytest
LINT        := .venv/bin/flake8
MYPY        := .venv/bin/mypy

LUIGID_HOST               := localhost
LUIGID_PORT               := 22222
LUIGI_WORKERS             := 1
LUIGI_CONFIG_PATH         := ./conf/luigi.cfg
BISCUIT_LOGGING_CONF      := ./conf/logging.yaml

luigi_opts = --scheduler-host $(LUIGID_HOST) --scheduler-port $(LUIGID_PORT) --workers $(LUIGI_WORKERS)
common_env = ENV=$(ENV) \
		AWS_DEFAULT_REGION=$(AWS_DEFAULT_REGION) \
		LUIGI_CONFIG_PATH=$(LUIGI_CONFIG_PATH) \
		BISCUIT_LOGGING_CONF=$(BISCUIT_LOGGING_CONF)

# info
.PHONY: info
info: 
		@echo 'setup: Setup environments by pipenv'
		@echo 'lint: Lint by flake8 and mypy'
		@echo 'test: Test by nose'

# setup
.PHONY: setup
setup: pipenv/install

PIPENV_OPTS := 
export PIPENV_VENV_IN_PROJECT := 1

.PHONY: pipenv/*
pipenv/install:
		$(PIPENV) install $(PIPENV_OPTS) --dev
pipenv/update:
		$(PIPENV) $(@F)
pipenv/graph:
		$(PIPENV) $(@F)
pipenv/check:
		$(PIPENV) $(@F)

# lint
.PHONY: lint*
lint: lint/flake8 lint/mypy
lint/flake8:
		$(LINT) biscuit tests
		@echo lint OK
lint/mypy:
		$(MYPY) biscuit tests
		@echo Type checking OK

# test
.PHONY: test
BISCUIT_LOGGING_CONF := ./conf/logging.test.yaml
test: 
		echo $(BISCUIT_LOGGING_CONF)
		$(common_env) $(PYTEST) tests

# run tasks
# ...
