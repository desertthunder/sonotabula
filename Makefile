.PHONY: devc help write server

help:
	@echo "Usage: make [target]"
	@echo ""
	@echo "Targets:"
	@echo "  server	- Start the application server"
	@echo "  write	- Start the documentation server"
	@echo "  devc	- Build the client dev server"
	@echo "  help	- Display this help message"

devc:
	@echo "Starting client dev server..."
	@cd client && bun dev

write:
	@echo "Starting docusaurus server..."
	@cd doc && bun start

server:
	@echo "Starting application server..."
	@python ./manage.py runserver
