.PHONY: help test serve

# PopQ's `make run` holds 8080.
PORT ?= 8081

help: ## List the available targets.
	@grep -hE '^[a-z-]+:.*##' $(MAKEFILE_LIST) | sed 's/:.*##/\t/' | expand -t 14

test: ## The full contract: every page parses, every local link resolves.
	@python3 scripts/check.py

serve: ## Preview the site at http://localhost:8081; PORT=… picks another port.
	@python3 -m http.server $(PORT)
