# Contributing

## Installation

System dependencies:
- Python 3.8+
- [Python Poetry](https://python-poetry.org/docs/)

1. Create a virtual environment.
2. Run `poetry install` to install the package.

### Troubleshooting

- If you're getting the error: `ModuleNotFoundError: No module named '_sqlite3'`, you need to install `libsqlite3-dev` (`sudo apt install libsqlite3-dev` on Ubuntu) and reinstall Python.

## Tests

Running the tests:

```
pytest
```

Running the tests with code coverage:

```
pytest --cov=easy_equities_client tests/
```

## Linting

With pre-commit:

- Install [pre-commit](pre-commit.com/).
- Run `pre-commit install`.
- Stage files.
- When you create a commit, pre-commit will automatically lint and check your staged files.
- Stage the files that were modified again.
- Repeat until no more pre-commit errors are raised.

Manually:

```
black .
flake8
```

## Type-checking

We use [MyPy](https://mypy.readthedocs.io/en/latest/index.html) for static type-checking. You can run it with:

```
mypy easy_equities_client tests
```

## Releasing a new version

1. Update [CHANGELOG.md](./CHANGELOG.md) following the [Keep a changelog](https://keepachangelog.com/en/1.0.0/) format.

2. Bump the version number (following [semantic versioning](https://semver.org/)):

```
bump2version < either: major / minor / patch >
```