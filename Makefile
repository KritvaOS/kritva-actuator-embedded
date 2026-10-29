# Kritva Actuator Embedded: make targets (Kritva Makefile standard, kritva-program v2/planning/standards/MAKEFILE_STANDARD.md)
PYTHON ?= python3
ROOT := $(CURDIR)
# A target is documented by `name: ## text` on its rule line; `##@ Name` starts a help group.
# An unimplemented gate exits 3 (NOT_IMPLEMENTED). It is never a pass.
.DEFAULT_GOAL := help
.PHONY: help

##@ Help
help: ## Show this list
	@awk 'BEGIN { FS = ":.*##"; printf "\nUsage: make <target> [VAR=value ...]\n" } \
	  /^##@/ { g = substr($$0, 5); next } \
	  /^[a-zA-Z0-9_.-]+:[^=].*##/ { if (g != "") { printf "\n%s\n", g; g = "" }; sub(/^ +/, "", $$2); printf "  %-24s %s\n", $$1, $$2 }' $(MAKEFILE_LIST)

##@ Checks
.PHONY: check check-bom check-status check-readme
check: check-bom check-status ## Run all checks
check-bom: ## Validate the electrical BOM schema
	$(PYTHON) scripts/check_bom.py --root $(ROOT)

check-status: ## Validate status/status.json (kritva-program status schema 2.0) against status/tasks.csv
	$(PYTHON) scripts/status/gen_status.py --root $(ROOT) --check

check-readme: ## Check README.md against the Kritva README standard (structure, metadata, local links)
	$(PYTHON) scripts/check_readme.py README.md --root $(ROOT)

##@ Gates (unimplemented gates exit 3)
define not_implemented
	@echo "NOT_IMPLEMENTED: $(1) has no tests yet; this is not a pass"; exit 3
endef

.PHONY: lint
lint: ## Static analysis and lint (NOT_IMPLEMENTED: exits 3)
	$(call not_implemented,lint)

.PHONY: test-unit
test-unit: ## Unit tests (NOT_IMPLEMENTED: exits 3)
	$(call not_implemented,test-unit)

.PHONY: test-integration
test-integration: ## Integration tests (NOT_IMPLEMENTED: exits 3)
	$(call not_implemented,test-integration)

.PHONY: test-regression
test-regression: ## Regression tests (NOT_IMPLEMENTED: exits 3)
	$(call not_implemented,test-regression)

.PHONY: test
test: ## All tests (NOT_IMPLEMENTED: exits 3)
	$(call not_implemented,test)

.PHONY: acceptance
acceptance: ## Acceptance gate (NOT_IMPLEMENTED: exits 3)
	$(call not_implemented,acceptance)

.PHONY: docs-check
docs-check: ## Documentation link and structure check (NOT_IMPLEMENTED: exits 3)
	$(call not_implemented,docs-check)

##@ Git
.PHONY: git_sync
git_sync: ## Switch to main, fast-forward from origin, prune, delete merged local branches
	@git switch main
	@git pull --ff-only --prune
	@git branch --format='%(refname:short)' | grep -vx main | xargs -r git branch -d
	@git log --oneline -3
