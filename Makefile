#################################################################################
# GLOBALS                                                                       #
#################################################################################

PROJECT_NAME = tech-challenge-fase-1
PYTHON_VERSION = 3.12
PYTHON_INTERPRETER = python

#################################################################################
# COMMANDS                                                                      #
#################################################################################


## Bootstrap the project: install Poetry, create env, install deps and pre-commit hooks
.PHONY: setup
setup:
	@echo ">>> Checking Poetry installation..."
	@if ! command -v poetry &> /dev/null; then \
		echo ">>> Poetry not found. Installing via pipx..."; \
		pipx install poetry; \
	else \
		echo ">>> Poetry already installed: $$(poetry --version)"; \
	fi
	@echo ">>> Setting up Python $(PYTHON_VERSION) environment..."
	poetry env use $(PYTHON_VERSION)
	@echo ">>> Installing dependencies..."
	poetry install
	@echo ">>> Installing pre-commit..."
	poetry run pip install pre-commit --quiet
	@echo ">>> Installing/updating pre-commit hooks..."
	poetry run pre-commit install
	poetry run pre-commit autoupdate
	@echo ">>> Setup complete. Activate the environment with:"
	@echo '    $$(poetry env activate)'


## Activate Poetry venv in current shell (usage: eval "$(make activate)")
.PHONY: activate
activate:
	@poetry env activate


## Install Python dependencies
.PHONY: requirements
requirements:
	poetry install




## Delete all compiled Python files
.PHONY: clean
clean:
	find . -type f -name "*.py[co]" -delete
	find . -type d -name "__pycache__" -delete


## Lint using ruff (use `make format` to do formatting)
.PHONY: lint
lint:
	ruff format --check
	ruff check

## Format source code with ruff
.PHONY: format
format:
	ruff check --fix
	ruff format



## Run tests
.PHONY: test
test:
	python -m pytest tests


## Set up Python interpreter environment
.PHONY: create_environment
create_environment:
	poetry env use $(PYTHON_VERSION)
	@echo ">>> Poetry environment created. Activate with: "
	@echo '$$(poetry env activate)'
	@echo ">>> Or run commands with:\npoetry run <command>"




#################################################################################
# PROJECT RULES                                                                 #
#################################################################################


## Make dataset
.PHONY: data
data: requirements
	$(PYTHON_INTERPRETER) tech_challenge_fase_1/dataset.py


#################################################################################
# Self Documenting Commands                                                     #
#################################################################################

.DEFAULT_GOAL := help

define PRINT_HELP_PYSCRIPT
import re, sys; \
lines = '\n'.join([line for line in sys.stdin]); \
matches = re.findall(r'\n## (.*)\n[\s\S]+?\n([a-zA-Z_-]+):', lines); \
print('Available rules:\n'); \
print('\n'.join(['{:25}{}'.format(*reversed(match)) for match in matches]))
endef
export PRINT_HELP_PYSCRIPT

help:
	@$(PYTHON_INTERPRETER) -c "${PRINT_HELP_PYSCRIPT}" < $(MAKEFILE_LIST)
