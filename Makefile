# Kritva Actuator Embedded - checks
PYTHON ?= python3
ROOT := $(CURDIR)
.PHONY: check check-bom
check: check-bom  ## Run all checks
check-bom:  ## Validate the electrical BOM schema
	$(PYTHON) scripts/check_bom.py --root $(ROOT)
