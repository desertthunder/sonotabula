# Backend

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

### Channels

Django Channels is used with `daphne` & redis, on top of the built-in ASGI application. This
is used for notifications about the status of tasks on the client side. Internally
the consumers listen for messages from Django signals, which are dispatched by
celery signals when a task starts, succeeds, or fails.

#### Channels (`live`) Models

1. `Notification`
2. `Acknowledgement`
3. `TaskResult`

#### Celery Results: `TaskResult`

These come from the `django_celery_results` package and are used to store the
results and metadata of tasks executed by Celery.

### Data Analysis

From the `audio-features` endpoint at Spotify, we return the following schema
of data:

```python
class TrackFeatures(BaseModel):
    """Track features for analysis."""

    id: str
    danceability: float
    energy: float
    key: int
    loudness: float
    mode: int # Modality - 0 for minor, 1 for major
    speechiness: float
    acousticness: float
    instrumentalness: float
    liveness: float
    valence: float
    tempo: float
    duration_ms: int
    time_signature: int
```

The `id` field is the `spotify_id` of the track.

An ongoing question is what fields are relevant to the user and how we can
use these attributes to provide value to the user as it pertains to
organizing their music.

Note: the pydantic models are used to clean and validate data before it is
saved to the database.

#### Analysis Models

Analysis in the context of the application isn't a true analysis of the data. It
is a persisted record of related objects and the data they contain. The `Analysis`
object stores the association between track features and the track itself, as well
as the overarching context of the collection (i.e., album, playlist, etc.).

A `Computation` object is related to its `Analysis` object. It stores calculations
and statistics about the audio features of a collection's tracks. A collection can
be a single track, album, or playlist.

#### Computation Data

- Superlatives:
    - Danceability
    - Energy
    - Loudness
    - Speechiness
    - Acousticness
    - Instrumentalness
    - Liveness
    - Valence
    - Tempo
    - Duration

- Averages: All of the above, with particular importance given to:
    - Tempo (fastest & slowest)
    - Valence (happiest & saddest)
    - Duration (longest & shortest)

- Counts:
    - Minor Key i.e., mode = 0
    - Major: mode = 1

## Authentication Middleware & Backends

Spotify's API implements the OAuth2 delegated authority flow. When the user
grants the application access, they're brought back to the app and the token is
stored and then encoded as a JWT. The JWT is stored in the React app's state.

### **Sign-up**: Client side route at `/signup`

- The sign-up button sends an empty `POST` request to the server at `/api/signup/`
    - The server redirects the user to the Spotify Authorization page.
    - The user logs in to spotify and authorizes the application.
        - In local development, the redirect uri is `http://localhost:8000/api/spotify_cb`
    - With the authorization code, the server requests an access token from Spotify.
    - Then the server creates a new user with the access token and refresh token,
    and the user's spotify id and email address.

### **Login**: Client side route at `/login`

- The login button sends an empty `PUT` request to the server at `/api/login/`
- Upon receiving the authorization code, the server requests an access token
from Spotify and fetches the user's information from the API. It users the
user's spotify id and email address to find the user in the database.
- After the user logs in, the user is redirected to the dashboard with a JWT token.
    - Client side route at `/dashboard?token=<JWT_TOKEN>`
    - The JWT token is stored in the browser's local storage.
    - The token is used to authenticate the user for all requests to the server
    with `simple-jwt`.

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

### Naming Things is Hard

Serializers are typically named after the model they are serializing, but the
model is named after the context it is in, as is common in Django applications.
This is especially common in the DRF + Django setup. I'm using DRF for some of
its built-ins, but have been using Pydantic for the majority of the application's
data validation and serialization, and de-serialization.

#### Solution

I'm in the process of renaming the serializers to match the model they are
serializing. There are a ton of repeated fields and code that *could* be abstracted
down the line. Additionally the child classes of `BaseModel` will be named after
the purpose they serve. So basically a `Serializer` is for an API endpoint, and
a `Block` is for an internal data structure and validation.

### Image Deletion/Cycling

Spotify's API returns image urls for albums and playlists but indicates that it
deletes them every day/the images expire. I think that one way to deal with this
is to dispatch a background task that refetches the image url from the API.

### Null/Empty Descriptions

Descriptions can be null if they haven't been updated recently (for unverified
playlists), so we shouldn't update descriptions if they are.

Can we update descriptions? Is that an allowed field in a mutate endpoint? *yes*

#### References

- [Playlist Details](https://developer.spotify.com/documentation/web-api/reference/get-playlist)
- [Update Playlist](https://developer.spotify.com/documentation/web-api/reference/change-playlist-details)
- [Playlist Image](https://developer.spotify.com/documentation/web-api/reference/get-playlist-cover)
