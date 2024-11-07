# Planning

This is a parking lot for feature concepts that have popped into my head and
from feedback I receive from my friends.

## Goals

Originally I was planning to deploy this application to a VPS, but as the project
expands, it may be best served as a docker image that can be self-hosted. In the
selfhosted/home lab community, there are a lot of interesting dashboards out there
and this *could* be one of them.

## Music Library Dashboard

One of my favorite things about Steam is that you can see Metacritic scores for
some games. In the music realm, albumoftheyear.org gets a frequent visit from me.
We can get music metadata from Musicbrainz and some albums will have wikipedia
pages with a *Critical Reception* block so we can use that. User submitted links
can likely help with this as well.

This could be an explorer section, in contrast to the library/browser section.
Spotify's API has endpoints to add tracks and albums to libraries as well.

Speaking of musicbrainz, `django-celery-beat` can schedule tasks to find data
on external sources.

### Search

The goal for search is to let user's transparently dig deeper in their playlists
for music they may want to listen to. Search is built using Django's built-in
field lookups.

#### Searchable Fields (for Playlist)

The proposed fields to search by are:
    - Playlist Name: `Playlist.objects.filter(name__icontains=query)`
    - Tracks Title: `Track.objects.filter(name__icontains=query)`
    - Artist Name: `Artist.objects.filter(name__icontains=query)`
    - Album Name: `Album.objects.filter(name__icontains=query)`

## These Docs

Since we're using conventional [commits](./development.md#angular-convention), a changelog
could be generated on releases. I might write my own.
