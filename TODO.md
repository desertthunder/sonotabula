# TODO

## Technical Debt

- [ ] Put flower in compose file
- [ ] Consolidate serializers
    - [ ] Better, more descriptive docstrings
    - [ ] Test for mappings methods
- [ ] Tests for tasks package
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
- [x] Hot reload for celery with [watchdog](https://watchfiles.helpmanual.io/cli/)

## Architecture

- [ ] Custom hook for description list
- [ ] Custom hook for table
- [ ] Wire up notification system with status from celery tasks

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
- [ ] Last played on Navbar
    - [ ] Query
    - [ ] Component
- [X] Playlists Page
    - [X] Datatable Component
    - [X] Track List Drawer

---

- [ ] Show computations on track list drawer
    - [ ] Min Max table
- [ ] Album Track List
