# splunk-cribl-utilities
A python package, cli and docker image of function and classes that are useful for migrating from splunk to cribl.

## Initial goal
In the longer term this package/ application will encompass more functionality, however for the moment the goal is to convert splunk conf toml files to the format required by cribl and to send them via the cribl API.
To do this we will make:
1. a python package (with unit tests etc.) for the required function
2. using the python package we will make a simple cli
3. we will make a Docker image using the cli so people can easily use it without installing a bunch of stuff first

## To run
- Make sure to have installed a python version >=3.13
- `docker compose up -d`
  - login and update admin password (default is `admin` and `admin`)
- `pip install -r requirements.txt`
- Example code without cli:
  - `cd cribl-utilities-cli`
  - `python example_usage_without_cli.py`

## To serve the docs
- `mkdocs serve`

## To run unit tests
- `docker compose up -d`
- `pip install -r requirements.txt`
- `cd cribl-utilities-cli`
- `pytest`

## Cleanup
- `docker compose down`

## Typer (cli) related
### Unix (macOS, Linux)
- `brew install pipx`
- `sudo pipx ensurepath --global` (this is to allow --global options)
- `pipx install poetry`
- `poetry config virtualenvs.in-project true` (this makes all venvs in the project)
### Windows
-  Open PowerShell as administrator
- `pip install pipx`
- `pipx ensurepath` 
-  Close PowerShell and open a new one
- `pipx install poetry`
- `poetry config virtualenvs.in-project true` (this makes all venvs in the project)

## cribl-utilities-cli CLI
- `poetry new cribl-utilities-cli`
- `cd cribl-utilities-cli`
- `poetry add typer`
- `poetry shell`
- `poetry build`
- `poetry install`
- `typer cribl_utilities_cli.main utils docs --output DOCS.md --name cribl-utilities-cli`

## Build and publish CLI
- make sure to have pipx and poetry installed and to be in the folder of the CLI itself
- `poetry shell`
- `poetry build`
- `poetry config http-basic.pypi <username> <password>` (run once)
- `poetry publish --build`