# Poetry package management

## Changing name of package

When chaging the package name:
1. Remove the `.venv` folder and the `poetry.lock`file.
1. Run `poetry lock --no-upgrade`
1. Run `poetry install`
1. Run `poetry run pre-commit install`

NB: above procedure might not be 100 % correct..
