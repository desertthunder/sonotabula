# Planning

This is a parking lot for feature concepts that have popped into my head and
from feedback I receive from my friends.

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

## These Docs

Since we're using conventional [commits](./commits.md), a changelog could be
generated on releases. I might write my own.
