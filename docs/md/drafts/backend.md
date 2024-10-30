# Backend Drafts

## Logging

Logging is handled by `loguru` on top of the standard library. In `manage.py`,
we disable some of the default loggers with a formatted logger.

## Proxying

Nginx with `mkcert` proxies requests to `https://local.dashspot.dev` to the
Django development server. This allows us to use HTTPS locally and put the client
and server behind the same custom domain.

## System

There are three contexts within the application's system:

1. Playback
2. Library
3. Browser

There is also a Core context that is shared between all three of these contexts.
This includes `services` and `libs` that are used across the entire application,
as well as a custom user model.

They have common components, but are separated by their own views, serializers,
and models. The system is designed to be modular, so that if we wanted to add
a new context, we could do so with minimal changes to the existing codebase.

- Client
    - `views`
    - `serializers`
- Persistence
    - `models`
    - `tasks`

### Serializers

There are two types of serializers being used in the application, both built on
top of Pydantic's `BaseModel` class. The first serializes Spotify API data to and
from the backend and the second is for database records. These are both leveraged
in the `library`, and `browser` contexts/apps, respectively.

### Tasks

Tasks are handled by Celery workers. Results are stored in the Postgres database,
and the task queue is managed by Redis. The task queue is used for asynchronous
calls to the database.

### Syncing

Serializing data from the Spotify API to the database and then client is done
with a combination of DRF (Django Rest Framework) and Pydantic. Pydantic validates
data before task processing as well.

When syncing a playlist, we're currently (October 28, 2024) only syncing Tracks
as opposed to Tracks and shows, so tracks are skipped.

### Library API Dispatch

Retrieve (GET to /:spotify_id) will dispatch a Celery task to take the response
data and save it to the database. So far this is implemented for Playlists and
Tracks. Tracks have an additional endpoint of `:spotify_id/data` that fetch and
then save audio features to the database. Thus *no* database calls aside from
what is already done by the authentication class are made in these views.

## Challenges

### Moving/Replacing the Custom User Model

In order to change the app that the custom user model was in, we had to reset
the entire migration history of the application. This is because the auth user
model is a major dependency of application models.

### Spotify API Pagination

The implementation of pagination is inconsistent across the Spotify API. For
most resources, the `next` field with an `offset` parameter is used. However,
for followed artists, a cursor is used and this requires the spotify ID of the
last page's artist to be passed in the next request (as `after`).
