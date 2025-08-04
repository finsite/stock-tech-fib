
.PHONY: help install test lint audit format clean clean-all compile upgrade-pins preflight precommit security bump docker-build sbom sign-image watch release licenses build-check coverage type-check pylint auditwheel ignore-check ci-check k8s-deploy slsa-sign tag freeze vault-login vault-lint docs-serve docs-build docs-deploy

help:
	@echo "Usage: make [target]"
	@echo "Targets:"
	@echo "  release         Run Commitizen changelog and bump version"
	@echo "  tag             Create and push Git tag using Commitizen version"
	@echo "  freeze          Export pinned versions to requirements-freeze.txt"
	@echo "  licenses        Generate markdown license report"
	@echo "  build-check     Validate built distributions with twine"
	@echo "  coverage        Run tests with HTML coverage report"
	@echo "  type-check      Run Pyright type checking"
	@echo "  pylint          Run Pylint with rating summary"
	@echo "  auditwheel      Check wheel portability using auditwheel"
	@echo "  ignore-check    Diff .gitignore vs .dockerignore and MANIFEST.in"
	@echo "  ci-check        Lint workflows using GitHub Super Linter"
	@echo "  k8s-deploy      Trigger Kubernetes deployment (requires make k8s)"
	@echo "  slsa-sign       Trigger SLSA provenance signing (GitHub CI only)"
	@echo "  vault-login     Log into Vault using AppRole"
	@echo "  vault-lint      Fetch secrets to validate Vault access"
	@echo "  docs-serve      Serve MkDocs site locally"
	@echo "  docs-build      Build MkDocs site"
	@echo "  docs-deploy     Deploy MkDocs site to GitHub Pages"
	@echo "  install        Install dependencies (core + dev)"
	@echo "  compile        Compile requirements.in and requirements-dev.in"
	@echo "  upgrade-pins   Upgrade all pinned versions in requirements.txt files"	
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

upgrade-pins:
	pip-compile --upgrade --output-file=requirements.txt requirements.in
	pip-compile --upgrade --output-file=requirements-dev.txt requirements-dev.in

lint:
	ruff . --ignore D100,D407,D414 && mypy src && yamlfix .

audit:
	pip check && pip-audit && deptry src

test:
	pytest --cov=src --cov-report=term-missing --cov-report=html \
		--disable-warnings --maxfail=3 --durations=10

test-unit:
	PYTHONPATH=src pytest -m unit

test-integration:
	PYTHONPATH=src pytest -m integration	

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
	cyclonedx-py requirements -i requirements.txt -o bom.json

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

# --- Documentation ---
docs-serve:
	mkdocs serve

docs-build:
	mkdocs build

docs-deploy:
	mkdocs gh-deploy

# --- Vault ---
vault-login:
	vault login -method=approle role_id="${VAULT_ROLE_ID}" secret_id="${VAULT_SECRET_ID}"

vault-lint:
	vault kv get ${VAULT_SECRET_PATH}

# --- Release & Versioning ---
release:
	cz changelog --dry-run
	cz bump

tag:
	VERSION=$(shell cz version --project) && git tag "v$$VERSION" && git push origin "v$$VERSION"

freeze:
	pip freeze > requirements-freeze.txt
	@echo "🔒 Current pinned packages exported to requirements-freeze.txt"

# --- License & Metadata ---
licenses:
	pip install pip-licenses
	pip-licenses --format=markdown --with-urls --output-file licenses.md
	@echo "📚 License report written to licenses.md"

build-check:
	pip install build twine
	python -m build
	twine check dist/*

# --- Coverage & Linting ---
coverage:
	pytest --cov=src --cov-report=term-missing --cov-report=html
	@echo "📈 HTML coverage report: htmlcov/index.html"

type-check:
	pyright

pylint:
	pylint src/

# --- CI / Workflow ---
auditwheel:
	docker run --rm -v $(PWD):/project -w /project quay.io/pypa/manylinux2014_x86_64 \
		bash -c "pip install build && python -m build && auditwheel show dist/*.whl"

ignore-check:
	@echo "🔍 Comparing .gitignore, .dockerignore, and MANIFEST.in"
	grep -v '^#' .gitignore | sort > .tmp.gitignore
	grep -v '^#' .dockerignore | sort > .tmp.dockerignore || true
	grep -v '^#' MANIFEST.in | sort > .tmp.manifest || true
	@echo "--- .gitignore not in .dockerignore:"
	comm -23 .tmp.gitignore .tmp.dockerignore || true
	@echo "--- .gitignore not in MANIFEST.in:"
	comm -23 .tmp.gitignore .tmp.manifest || true

ci-check:
	docker run --rm -v $(PWD):/tmp/github github/super-linter:v6 \
	-e VALIDATE_YAML=true \
	-e GITHUB_TOKEN=${GITHUB_TOKEN:-fake}

# --- Deployment ---
k8s-deploy:
	@echo "🚀 Running Kubernetes deployment"
	make k8s || echo "⚠️ 'make k8s' script not found. Define if needed."

slsa-sign:
	@echo "🔐 SLSA provenance signing triggered via GitHub CI only (see .github/workflows)"
