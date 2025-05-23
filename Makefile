.PHONY: help install test lint audit format clean compile preflight

help:
	@echo "Usage: make [target]"
	@echo "Targets:"
	@echo "  install      Install dependencies (core + dev)"
	@echo "  compile      Compile requirements.in and requirements-dev.in"
	@echo "  lint         Run ruff, mypy, and YAML formatters (non-destructive)"
	@echo "  audit        Run pip check, pip-audit, and deptry"
	@echo "  test         Run pytest with coverage and HTML report"
	@echo "  format       Auto-format using black, ruff --fix, and yamlfix"
	@echo "  preflight    Run compile, format, lint, audit, and pre-commit hooks"
	@echo "  clean        Remove __pycache__ and .pyc files"

install:
	pip install -r requirements.txt
	pip install -r requirements-dev.txt

compile:
	pip-compile --upgrade requirements.in
	pip-compile --upgrade requirements-dev.in

lint:
	ruff . --ignore D100,D407,D414 && mypy src && yamlfix .

audit:
	pip check && pip-audit && deptry src

test:
	pytest --cov=src --cov-report=term-missing --cov-report=html

format:
	black . && ruff . --fix && yamlfix .

preflight: compile format lint audit
	pre-commit run --all-files

clean:
	find . -type d -name "__pycache__" -exec rm -r {} + || true
	find . -name "*.pyc" -delete || true
