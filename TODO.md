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
- Put flower in compose file
- Hot reload for celery with [watchdog](https://watchfiles.helpmanual.io/cli/)

## Server Side

- [X] Expanded Playlist Structure
- [X] Expanded Playlist Endpoint
    - [X] Service
    - [X] View
- [ ] Home page stats Endpoint

## Client Side (Web)

- [ ] Figure out how to deploy docs to netlify
- [ ] Last played data fetching and display
