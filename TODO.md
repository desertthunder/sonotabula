# TODO

## Technical Debt

- Tests for tasks package
- Reused serializer code across packages. Create a single serializer package
that covers each database model.
    1. `api.libs`
    2. `api.models`
    3. `api.services`
- Useless views (expand playlist) - this could actually be a single task
- Service Structure?
    - Authentication
    - Library
    - Analysis
- Complete test coverage for services package

## Server Side

- [X] Expanded Playlist Structure
- [X] Expanded Playlist Endpoint
    - [X] Service
    - [X] View
- [ ] Top Items Endpoint

## Client Side (Web)

- [ ] Figure out how to deploy docs to netlify
- [ ] Last played data fetching and display
