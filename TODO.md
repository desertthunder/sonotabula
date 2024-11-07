# TODO.md

Follows `todo.txt` format.

```plaintext
{completion} ({priority}) {completed_date} {creation_date} {TASK} +{project} @{context} {key:value}
```

- Priority: Now or Later/1 or 0
- Project: basically an epic
- Context: "Project" (here it's Sonotabula)
- Custom Props (key:value):
    - type:`{type}` - test, features, chore, etc. (match commit types in [`commitlint.config.js`](./commitlint.config.js))

## Epics

- [x] 00 - Refactor init
- [ ] 01 - Browser Refactor & Real-time updates
- [ ] 02 - Data visualization
- [ ] 03 - Static pages
- [ ] 04 - Deployment
- [ ] 05 - Musicbrainz integration

## TODO

- [ ] (1) 2024-10-30 create real-time django app +browser-refactor @Sonotabula type:build
- [ ] (1) 2024-10-30 move /api/browser endpoints to browser app +browser-refactor @Sonotabula type:build
- [ ] (0) 2024-10-30 test endpoints in browser app +browser-refactor @Sonotabula type:test
- [ ] (0) 2024-10-30 add tests for authentication flow +browser-refactor @Sonotabula type:test
- [ ] (0) 2024-10-30 fix authentication flow on client +browser-refactor @Sonotabula type:fix
- [ ] (0) 2024-10-30 design new browser views +browser-refactor @Sonotabula type:feat(ui)
