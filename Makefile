################################################################################
# Makefile for the CV generation process 	                                   #
################################################################################
# The following Makefile wraps all commands required to generate the CV from   #
# the source data and template, as well as helpers and prerequisites.          #
# To get started run `make`, or `make [command]` to run a specific command.    #
################################################################################
# Full source on GitHub: https://github.com/horia-delicoti/cv  			 	   #
# Licensed under the MIT License, ⓒ Horia Delicoti 2025 <horia.delicoti.com>  #
################################################################################

# Define variables for common paths
PYTHON := $(shell which python3 2>/dev/null || which python)
VENV := .venv
PYTHON_VENV := $(VENV)/bin/python3
PIP := $(PYTHON_VENV) -m pip
REQUIREMENTS := lib/requirements.txt
SCHEMA := schema.json
RESUME := resume.yaml

# show help if no target is given
.PHONY: default
default: 
	@echo "No targets provided. Run 'make help' for available targets."

# Fallback for unknown targets
.PHONY: .DEFAULT
.DEFAULT: 
	@echo "❌ Unknown target. Run 'make help' for available targets."

# Makefile help in man-page style
.PHONY: help
help:
	@echo "CV GENERATION MAKEFILE"
	@echo
	@echo "NAME"
	@echo "    make - automate building, validating, and compiling the CV"
	@echo
	@echo "SYNOPSIS"
	@echo "    make [TARGET]"
	@echo
	@echo "DESCRIPTION"
	@echo "    Available targets:"
	@grep -E '^[a-zA-Z0-9 -]+:.*#' Makefile | sort | while read -r l; do printf "    \033[1;32m$$(echo $$l | cut -f 1 -d':')\033[00m:$$(echo $$l | cut -f 2- -d'#')\n"; done
	@echo
	@echo "EXAMPLES"
	@echo "    make all       # run the default workflow (install + validate)"
	@echo "    make install   # install dependencies"
	@echo "    make validate  # validate resume against schema"

.PHONY: venv
venv: # create new VENV for Python if it doesn't exist
	@echo "🐍 Creating virtual environment for Python..."
	$(PYTHON) -m venv $(VENV)
	$(PIP) install --upgrade pip setuptools

.PHONY: install 
install: # install required Python packages
	@echo "📦 Installing required Python dependencies..."
	$(PYTHON_VENV) -m pip install -r $(REQUIREMENTS)

.PHONY: validate 
validate: # validate the YAML resume against the JSON schema
	$(PYTHON_VENV) lib/validate.py --resume $(RESUME) --schema $(SCHEMA)

.PHONY: all
all: # install deps, validate, generate, compile, and clean up
	venv install validate
