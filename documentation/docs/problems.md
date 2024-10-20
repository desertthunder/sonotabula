# Problems

Spotify's API returns image urls for albums and playlists but indicates that it
deletes them every day/the images expire. I think that one way to deal with this
is to dispatch a background task that refetches the image url from the API.

Descriptions can be null if they haven't been updated recently (for unverified
playlists), so we shouldn't update descriptions if they are.

Can we update descriptions? Is that an allowed field in a mutate endpoint? *yes*

## References

- [Playlist Details](https://developer.spotify.com/documentation/web-api/reference/get-playlist)
- [Update Playlist](https://developer.spotify.com/documentation/web-api/reference/change-playlist-details)
- [Playlist Image](https://developer.spotify.com/documentation/web-api/reference/get-playlist-cover)
