# Django Server Architecture

## Codebase

The Django application is structured as follows:
    - `server`
    - `api`
    - `apps`
    - `browser`
    - `library`

The web client is in `web` and the documentation is called `docs`.

## ASGI Server

Made with `daphne` (and `uvicorn` eventually).

Real time communication is done with `channels`, represented with three models:
    1. `Notification`
        - A wrapper around a message
    2. `Resource`
    3. `Operation`

The asgi application sends a `Notification` to the client, which acknowledges it.
A record of this is created (`Acknowledgement` model).
