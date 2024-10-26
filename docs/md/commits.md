---
sidebar_position: 3
---
# Contributing

The main repository follows the [Conventional Commits](https://www.conventionalcommits.org/en/v1.0.0/) specification.

In order to enforce, this, commitlint is used.

Example of a good commit message structure:

```bash
git commit -m "type(scope?): message"
```

## Angular Convention

Valid Types:

- `fix` and `feat`
- `build`, `ci`, `docs`, `style`, `refactor`, `perf`, `test`
- `!` after the type/scope to indicate a breaking change

Scopes (not enforced):

- `api` - for changes to the exposed REST API (can be views or serializers)
- `services` - for changes to the services provided by the backend
- `database` - for changes to the database schema/model code
- `infra` - for changes to the infrastructure code (docker, compose, etc.)
- `web` - for changes to the web client
