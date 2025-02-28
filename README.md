# CriblUtilities
CriblUtilities is a Python CLI package that streamlines migration to Cribl Stream and validates configurations. With minimal setup, it transfers configurations from existing tools to Cribl Stream. It also integrates with GitOps workflows to verify naming conventions and file formats before implementing changes.

## Other packages
[PyPI](https://pypi.org/project/cribl-utilities/)

## Functionality
- Setup Cribl environment variables
- Convert splunk conf toml files to the format required by cribl
- Send the converted files via the cribl API
- Check if Cribl .yml files in cribl-config adhere to YAML linting
- Check if Cribl .yml files in cribl-config adhere to a given regex naming convention

## Cribl configuration 
A local Cribl user needs to be created. This user should minimally have the role: stream_editor.

## Python package usage
- `docker compose up -d`
- `pip install cribl-utilities`
- `cribl-utilities --help`

## Run example usage without installing the package
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
- `cd cribl-utilities`
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

## cribl-utilities CLI
- `poetry new cribl-utilities`
- `cd cribl-utilities`
- `poetry add typer`
- `poetry shell`
- `poetry build`
- `poetry install`
- `typer cribl_utilities.main utils docs --output DOCS.md --name cribl-utilities`

## Build and publish CLI
- make sure to have pipx and poetry installed and to be in the folder of the CLI itself
- `poetry shell`
- `poetry build`
- `poetry config http-basic.pypi <username> <password>` (run once)
- `poetry publish --build`
