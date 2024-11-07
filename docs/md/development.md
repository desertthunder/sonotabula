# Development Process

## Testing

Because of the reliance on external services, the testing process uses mocks
to simulate the behavior of the Spotify API. Because of this, SpotifyAPI integration
is encapsulated in adapters/a service layer that can be easily swapped out for
calls to `unittest.mock.patch`. Most tests in the application are either view tests
or manager tests.

## Authoring Commits

The main repository follows the [Conventional Commits](https://www.conventionalcommits.org/en/v1.0.0/) specification.

In order to enforce, this, commitlint is used.

Example of a good commit message structure:

```bash
git commit -m "type(scope?): message"
```

### Angular Convention

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

## Documentation

The documentation built with docusaurus and is deployed to netlify on commits to main.
There are also dev deployments that are triggered on commits to any branch with an
open PR. See the docusaurus docs for more information on the process [here](https://docusaurus.io/docs/deployment#deploying-to-netlify).

## Code Style

Code style on the back-end is enforced by Ruff and a number of Flake8 plugins.
The `ruff.toml` file is in the root of the repository. Docstrings are also enforced,
but I am reconsidering the usefulness of this, as I've ended up with docs that just
repeat the function signature or the class's name. Most helpful have been BugBear, and Mccabe.

The front-end uses ESLint with plugins for TypeScript & React Query.
