# Document Query Tool

There is a command line option and a UI option. To use the latter, run `uvicorn fastapi_app:app --reload`.

To run the command line option, run `python -m docucite.cli`.

## Getting started

## App structure

The app is structured into the layers `api`, `app`, `services`, and `model`.

The structure is

```
├── docs
├── docucite
├── notes
├── static
├── tests
    └──

```

## Development

Install dependencies with `pip install -r requirements_dev.txt`.

All code in the main folder `docucite` must be tested and of high quality.

## Code quality

Before submitting a PR, make sure the code in `docucite` is clean. We use the three tools:

`pylint docucite/`
`black docucite/`
`mypy docucite/ --ignore-missing-imports --disable-error-code "annotation-unchecked""`

## Testing
