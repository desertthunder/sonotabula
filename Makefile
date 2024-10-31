.PHONY: devc help write server test shell worker flower

help:
	@echo "Usage: make [target]"
	@echo ""
	@echo "Targets:"
	@echo "  server	- Start the application server"
	@echo "  shell	- Start the Django shell"
	@echo "  worker	- Start the Celery worker"
	@echo "  flower	- Start the Celery Flower dashboard"
	@echo "  write	- Start the documentation server"
	@echo "  devc	- Build the client dev server"
	@echo "  test	- Run the test suite"
	@echo "  help	- Display this help message"

devc:
	@echo "Starting client dev server..."
	@cd client && pnpm dev

write:
	@echo "Starting docusaurus server..."
	@cd docs && pnpm start

server:
	@echo "Starting application server..."
	@python ./manage.py runserver

test:
	@echo "Running test suite..."
	@python ./manage.py test --keepdb -v 2

shell:
	@echo "Starting shell..."
	@python ./manage.py shell

worker:
	@echo "Starting Celery worker..."
	@watchmedo auto-restart --patterns='**/*.py' --recursive -- celery -A server worker -l info

flower:
	@echo "Starting Celery Flower dashboard..."
	@celery -A server flower
