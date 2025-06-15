
.PHONY: help install test lint audit format clean clean-all compile preflight precommit security bump docker-build sbom sign-image watch

help:
	@echo "Usage: make [target]"
	@echo "Targets:"
	@echo "  install        Install dependencies (core + dev)"
	@echo "  compile        Compile requirements.in and requirements-dev.in"
	@echo "  lint           Run ruff, mypy, and YAML formatters (non-destructive)"
	@echo "  audit          Run pip check, pip-audit, and deptry"
	@echo "  test           Run pytest with coverage and HTML report"
	@echo "  format         Auto-format using black, ruff --fix, and yamlfix"
	@echo "  preflight      Run compile, format, lint, audit, and pre-commit hooks"
	@echo "  precommit      Run all pre-commit hooks with diff reporting"
	@echo "  security       Run Bandit security scan"
	@echo "  bump           Run Commitizen version bump"
	@echo "  docker-build   Build Docker image using current directory name as tag"
	@echo "  clean          Remove __pycache__ and .pyc files"
	@echo "  clean-all      Remove all build and coverage artifacts"
	@echo "  sbom           (Optional) Generate SBOM using syft"
	@echo "  sign-image     (Optional) Sign Docker image using cosign"
	@echo "  watch          (Optional) Run pytest in watch mode (requires ptw)"

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

precommit:
	pre-commit run --all-files --show-diff-on-failure

security:
	bandit -r src -lll -iii

bump:
	cz bump --yes

docker-build:
	docker build -t $(shell basename $(PWD)):latest .

clean:
	find . -type d -name "__pycache__" -exec rm -r {} + || true
	find . -name "*.pyc" -delete || true

clean-all: clean
	rm -rf .mypy_cache .pytest_cache .coverage htmlcov dist build

# -----------------------------------------------------------------------------
# Repo Sync Utilities (from repo-utils-shared)
# -----------------------------------------------------------------------------

sync:
	@echo "🔍 Running dry-run sync (no changes applied)..."
	python sync_if_needed.py

sync-apply:
	@echo "🚀 Applying sync to all repositories..."
	python sync_if_needed.py --apply && echo "✅ Sync complete. Changes logged in sync.log"

# -----------------------------------------------------------------------------
# Attestation and SBOM Targets
# -----------------------------------------------------------------------------

sbom-py:
	cyclonedx-py -o bom.json

sbom-image:
	syft . -o spdx-json > sbom.spdx.json

attest: sbom-py sbom-image audit

# -----------------------------------------------------------------------------
# Optional Utilities (enable as needed)
# -----------------------------------------------------------------------------

# sign-image:
# 	cosign sign $(shell basename $(PWD)):latest

# watch:
# 	ptw --onfail "notify-send 'Test failed!'"
