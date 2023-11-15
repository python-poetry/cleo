# Contribute to Cleo

## Project Management

The Cleo project is managed by [Poetry](https://python-poetry.org/). You need to install it first:

```bash
pipx install poetry
```

For other installation methods, please refer to [Poetry's documentation](https://python-poetry.org/docs/#installation).

After the installation, install the project and dependencies:

```bash
poetry install
```

## Run the Tests

```bash
poetry run pytest
```

## Code Style and Linters

We use [Ruff](https://github.com/charliermarsh/ruff) as the linter and formatter.
It is integrated into [pre-commit](https://pre-commit.com/). You can enable it by:

> NOTICE: `pre-commit` is declared as one of development dependencies of Cleo. If you don't have `pre-commit` installed globally, prepend the commands in this section with `poetry run`

```bash
pre-commit install
```

and run the checks by:

```bash
pre-commit run --all-files
```

### News fragments

When you make changes such as fixing a bug or adding a feature, you must add a news fragment describing
your change. News fragments are placed in the `news/` directory, and should be named according to this pattern: `<issue_num>.<issue_type>.md` (e.g., `566.bugfix.md`).

> NOTICE: If your change doesn't have an issue, please use PR number in place of `<issue_num>`

#### Issue Types

- `break`: Breaking changes
- `feat`: Features & Improvements
- `bugfix`: Bug fixes
- `docs`: Changes to documentation
- `deps`: Changes to dependencies
- `removal`: Removals or deprecations in the API
- `misc`: Miscellaneous changes that don't fit any of the other categories

The contents of the file should be a single sentence in past tense that describes your changes (e.g., `Added CONTRIBUTING.md file.`).
See entries in the [Change Log](/CHANGELOG.md) for more examples.
