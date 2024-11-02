# Backend Drafts

## Data Model

Audio Features are the core Spotify resource utilized by this application. These
objects are persisted as `TrackFeatures` and collected as `Analysis` objects. Aggregating
the data (superlatives, averages, etc.) is done in a summary model, called `Computation`.

Operations are done in the `AnalysisManager` class and computations are conducted by
querying a collection of tracks (or a single track) and then aggregating with
a pandas DataFrame. Part of the reason for using `pandas` is to leverage its
`groupby` functionality and exporting/importing capabilities.

### Managers

Managers are used to perform creation queries on the database, as atomically and
efficiently as possible. Based on input data, the transactions are idempotent
as well.

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

Tasks are a mix of classes to store operation state, and functions for the worker
to discover and execute. The tasks are stored in the `tasks` module of its respective
app/context.

Pausing tasks is done by adding a simple wrapper around `time.sleep`. In the
browser tasks module this is the `delay_execution` function in between sync
and analysis tasks.

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

## Naming Things is Hard

Serializers are typically named after the model they are serializing, but the
model is named after the context it is in, as is common in Django applications.
This is especially common in the DRF + Django setup. I'm using DRF for some of
its built-ins, but have been using Pydantic for the majority of the application's
data validation and serialization, and de-serialization.

### Solution

I'm in the process of renaming the serializers to match the model they are
serializing. There are a ton of repeated fields and code that *could* be abstracted
down the line. Additionally the child classes of `BaseModel` will be named after
the purpose they serve. So basically a `Serializer` is for an API endpoint, and
a `Block` is for an internal data structure and validation.
