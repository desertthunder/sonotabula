---
sidebar_position: 2
---

# Architecture

## Data Model

Under construction. 🚧

## API Structure

Under construction. 🚧

## Background Tasks

Under construction. 🚧

## Web

Under construction. 🚧

## Mobile

Under construction. 🚧

## Playback API

Playback endpoints are all synchronous.

## Library API

Library endpoints can occur either synchronously or asynchronously.
    - **Asynchronous endpoints** return the newest data from the API (but still update the
    record in the database).
    - **Synchronous Endpoints** return whatever is in the database.
    - This is based on the `sync` param.
These endpoints also *only* return lists.

### Endpoints

1. [Playlists](./playlists.md)
The asynchronouse playlist endpoint is visible on the home page of the dashboard.
For synchronous, it is visible on the playlist page.

2. Tracks
3. Artists
4. Albums

## Analysis

1. Track
2. Playlist

## Database

1. Playlist
2. Track
3. Artist
4. Album
