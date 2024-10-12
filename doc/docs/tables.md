# Tables

This page describes the data tables present on the client, as well as list views
for library resources.

Default sorting for playlists: Analyzed first, then synced, alphabetical

## Filter State

Filter state is stored in the URL.

| Name     | Query Param | Filter Class             |
|---       | ---         | ---                      |
| search   | `q`         |                          |
| sort     | `sort`      |                          |
| analyzed | `stats`     |                          |
| synced   | `synced`    |                          |

## Filter Classes

These should take a queryset, and a DRF request object to return the records that
are requested. This is heavily inspired by `django-filter`.
