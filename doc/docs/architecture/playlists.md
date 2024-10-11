# Playlists

Spotify Docs: [Playlists](https://developer.spotify.com/documentation/web-api/reference/playlists/)

The playlist endpoints leverage the paginated saved playlist response from the
Spotify API.

## Async

## Sync

List Endpoint: `/api/sync/playlists`
Retrieve Endpoint: `/api/sync/playlists/{public_id}`

In order for the `public_id` to be retrieved, the user must have saved the
playlist to the database already.

Params: `offset` (won't work until all playlists are synced)
By default, the playlists are sorted by the date they were added to the database.
Eventually, the user will be able to sort by name, date added, and other fields.

When making the request to Spotify, 25 records will be retreived.
The user can then paginate through the records.

```json
{
    "page": 1,
    "total_pages": 2,
    "total_results": 50,
    "offset": 0,
    "data": []
}
```

### Task Dispatch

The first task is dispatched when the user goes to the playlist page (`/playlists`).
It will occur based on whether or not the total count of playlists matches
the user's total count of playlists.

1. `sync_playlists` - This task will retrieve all of the playlists from Spotify
and save them to the database.
2. `sync_playlist_tracks` - This task will retrieve all of the tracks from Spotify
and save them to the database.
3. Artists & Albums (Group)
    - `sync_playlist_artists` - This task will retrieve all of the artists from Spotify
and save them to the database.
    - `sync_playlist_albums` - This task will retrieve all of the albums from Spotify

## Requirements

- [ ] Batch create query for playlists
    - [ ] Paginated API Request to `/me/playlists`
    - [ ] Sync playlists task
- [ ] Batch create query for playlist tracks
    - [ ] Version 1: Use the tracks object from the playlist object
    - [ ] Sync playlist tracks task
- [ ] Batch create query for playlist artists
    - [ ] Version 1: Use the album object from the track object
    - [ ] Sync playlist artists task
- [ ] Batch create query for playlist albums
    - [ ] Version 1: Use the album object from the track object
    - [ ] Sync playlist albums task

## View Layer

The playlist page will display the playlists in a data table. The user will be able to
search by
    1. Playlist Name
    2. Song Title
    3. Artist Name
    4. Album Name
It will include the following columns:
    1. Playlist Name
    2. Number of Tracks
    3. Analyzed?
    4. Date Added
    5. Actions
        - View Playlist
        - View Playlist on Spotify
        - Analyze Playlist

## Future

- A websocket for a notification when the sync is complete
