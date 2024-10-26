# Search

The goal for search is to let user's transparently dig deeper in their playlists
for music they may want to listen to. Search is built using Django's built-in
field lookups.

## Searchable Fields (for Playlist)

The proposed fields to search by are:
    - Playlist Name: `Playlist.objects.filter(name__icontains=query)`
    - Tracks Title: `Track.objects.filter(name__icontains=query)`
    - Artist Name: `Artist.objects.filter(name__icontains=query)`
    - Album Name: `Album.objects.filter(name__icontains=query)`

### UI

If search doesn't return any hits, I think it be best to leave the table as is rather than
render empty rows.

## Future

Lyric search would be cool.
