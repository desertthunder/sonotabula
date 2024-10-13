# TODO

## Technical Debt

- Tests for tasks package
- [x] Reused serializer code across packages. Create a single serializer package
that covers each database model.
    1. `api.libs`
    2. `api.models`
    3. `api.services`
- [x] Useless views (expand playlist) - this could actually be a single task
- [x] Service Structure?
    - Authentication
    - Library
    - Analysis
- [x] Complete test coverage for services package
- [ ] Put flower in compose file
- [x] Hot reload for celery with [watchdog](https://watchfiles.helpmanual.io/cli/)

## Server Side

- [X] Expanded Playlist Structure
- [X] Expanded Playlist Endpoint
    - [X] Service
    - [X] View
- [x] Home page stats Endpoint
- [X] Playlist Tracks List
    - [x] Playlist Tracks Filters
    - [X] Playlist Track Serializer
        - [X] Playlist Track Features Serializer

## Client Side (Web)

- [x] Figure out how to deploy docs to netlify
- [ ] Last played
    - [ ] Query
    - [ ] Component
- [ ] Playlists Page
    - [ ] Datatable Component
    - [ ] Track List Drawer
