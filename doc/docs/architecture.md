# Architecture

## Playback

## Library

Library endpoints can occur either synchronously or asynchronously.
    - **Asynchronous endpoints** return the newest data from the API (but still update the
    record in the database).
    - **Synchronous Endpoints** return whatever is in the database.
    - This is based on the `sync` param.
These endpoints also *only* return lists.

1. Playlists

    - Fetch library playlists
        - Complete the request for the maximum allowed (50) if synchronous
        - Just return the limit if it is an async call.
        - *Main Task*: Fetch *all* playlists, update the record if the snapshot ID has changed.
            - Return type: None
            - For each task, dispatch the track API call after persisting the playlist
            to the database.
        - *Task 2*: Fetch the playlist's tracks
            - Dispatch track analysis task
        - *Task 3*: Fetch track metadata
            - Fetch track features
            - Persist metadata, then track features
            - Create an analysis record

2. Tracks

3. Artists

4. Albums

## Analysis

- Playlist Analysis
    - Checks for an analysis record
    - If it doesn't exist, create one.

## Database

These are "expanded" requests for single records
