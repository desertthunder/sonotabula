
.PHONY: devc help

help:
	@echo "Usage: make [target]"
	@echo ""
	@echo "Targets:"
	@echo "  devc	- Build the client dev server"
	@echo "  help	- Display this help message"

devc:
	@echo "Starting client dev server..."
	@cd client && bun dev
