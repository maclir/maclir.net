.PHONY: help test serve

help: ## List the available targets.
	@grep -hE '^[a-z-]+:.*##' $(MAKEFILE_LIST) | sed 's/:.*##/\t/' | expand -t 14

test: ## The full contract: every page parses, every local link resolves.
	@python3 scripts/check.py

serve: ## Preview the site at http://localhost:8080.
	@python3 -m http.server 8080
