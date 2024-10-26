# Spotify Dashboard

[![Netlify Status](https://api.netlify.com/api/v1/badges/a2dbf0df-0390-4635-98aa-ab2dfe272e98/deploy-status)](https://app.netlify.com/sites/dashspot-dev/deploys)

DashSpot is a dynamic visualizing dashboard designed to explore and analyze
Spotify libraries meant to be like an itunes style library browser.

It is built with Django, Postgres, Celery, and React on top of the Spotify API.

By adding additional integration with Wikipedia and MusicBrainz, DashSpot builds
a comprehensive database of music metadata relevant to them.

![DashSpot Screenshot](./doc/static/img/screencap.png)

Check out the [docs](https://dashspot-dev.netlify.app/)!

## Setup

Copy the sample `.env` file and fill in the necessary environment variables. I
use bitwarden to manage my secrets.

```bash
cp .env.sample .env
```

### Running the application

1. `docker-compose up` for the postgres database & redis server
2. `./manage.py runserver` to start the Django server (don't forget to apply
   migrations before you start the server)
3. `celery -A server worker -l INFO`
4. `celery -A server flower`

Alternatively, you can use the `Makefile` to run the application (see `make help`).
Running the workers through the `Makefile` has hot-reloading with watchdog (`watchmedo`).

```bash
docker compose up
make server
make worker
make flower
```

## Back-end

This is a Django application that uses REST framework for serializing and
deserializing objects.

## Front-end

This dashboard is built using React & Tailwind.

## Documentation

### Design

#### Colors

The colors are inspired by the Spotify brand colors and come from the base
colors in the Tailwind CSS framework.

Primary: Emerald 600
Secondary: Sky 500
Text: Zinc 800
Background: Neutral 200

## Spotify API

The core integration is built with Spotify.

### Attribution

From the [top tracks](https://developer.spotify.com/documentation/web-api/reference/#endpoint-get-users-top-artists-and-tracks) endpoint documentation:

> Please keep in mind that metadata, cover art and artist images must be
> accompanied by a link back to the applicable artist, album, track, or playlist
> on the Spotify Service.
>
> You must also attribute content from Spotify with the logo.
