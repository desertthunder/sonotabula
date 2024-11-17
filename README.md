# Sonotabula

[![Netlify Status](https://api.netlify.com/api/v1/badges/a2dbf0df-0390-4635-98aa-ab2dfe272e98/deploy-status)](https://app.netlify.com/sites/sonotabula/deploys)

Sonotabula is a dynamic visualizing dashboard designed to explore and analyze
Spotify libraries meant to be like an iTunes style library browser.

It is built with Django, Postgres, Celery, and React on top of the Spotify API.

By adding additional integration with Wikipedia and MusicBrainz, Sonotabula builds
a comprehensive database of music metadata relevant to them.

| <center>Playlist Browser</center>                    |
| ---------------------------------------------------- |
| ![Sonotabula Screenshot](./docs/static/img/demo.png) |

Check out the [docs](https://sonotabula.netlify.app/)!

## Overview

The primary goal of this application is to enhance the library browsing experience for Spotify users.
We went from iTunes and Winamp to many iterations of Spotify, and the current iteration of the latter
does little to give you control over the exploration of new music, or the rediscovery of what
you've saved.

### Features

1. Better search and filtering capabilities - if you search for a track, you should be able to see
what playlists it's in, what albums it's in, and what artists are associated with it.
2. Better visualization of your library - you should be able to see what genres you listen to, what
artists you listen to, and what tracks you listen to, as well as some of the audio features of those
tracks.
3. Better browsing - instead of a giant sidebar being the only way to smoothly navigate your library.
Many applications do a great job of this for locally saved music, and I'd like to bring that to Spotify.

## Setup

Copy the sample `.env` file and fill in the necessary environment variables. I
use bitwarden to manage my secrets.

```bash
cp .env.sample .env
```

### Virtual Environment

```bash
asdf install # Optional, relies on .tool-versions
```

```bash
pip install poetry
poetry env use python 3.12
source $(poetry env info --path)/bin/activate
poetry install
```

### Database

The settings module relies on a database environment variable. How you set this
up is up to you. I use a shared docker container for postgres databases on my
local machines. What's important is that the server is running and the database
is created, with up to date credentials in the `.env` file.

```bash
./manage.py migrate
```

### Running the application

1. Make sure you set the Spotify API credentials in the `.env` file, and setup
   the Spotify API callback URL in the Spotify Developer Dashboard.
2. `./manage.py runserver` to start the Django server (don't forget to apply
   migrations before you start the server)
3. `celery -A server worker -l INFO`

Alternatively, you can use the `Makefile` to run the application (see `make help`).
Running the workers through the `Makefile` has hot-reloading with watchdog (`watchmedo`).

```bash
make server
make worker
make flower # Optional, for monitoring the workers
```

### Tests

```bash
coverage run manage.py test
```

To view the coverage report in the browser (the file is located at `htmlcov/index.html`):

```bash
coverage html
```

## Spotify API

The core integration is built with Spotify.

### Attribution

From the [top tracks](https://developer.spotify.com/documentation/web-api/reference/#endpoint-get-users-top-artists-and-tracks)
endpoint documentation:

> Please keep in mind that metadata, cover art and artist images must be
> accompanied by a link back to the applicable artist, album, track, or playlist
> on the Spotify Service.
>
> You must also attribute content from Spotify with the logo.
