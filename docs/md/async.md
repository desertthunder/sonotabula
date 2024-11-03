# Asynchronous Architecture

Using Django channels, signals, Celery, and Redis, a real-time application built
on top of the ASGI protocol is used to handle notifications of new operations
completed by the system.

## Data Model

1. `Notification`
2. `Acknowledgement`
3. `TaskResult`

### Celery Results: `TaskResult`

These come from the `django_celery_results` package and are used to store the
results and metadata of tasks executed by Celery.
