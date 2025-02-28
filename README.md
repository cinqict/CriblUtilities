# 🚀 CriblUtilities
CriblUtilities is a Python CLI package that streamlines migration to Cribl Stream and validates configurations. With minimal setup, it transfers configurations from existing tools to Cribl Stream. It also integrates with Cribl GitOps workflows to verify naming conventions and file formats before implementing changes.


## 🫶 Functionality
| **Function** | **Explanation**                       |
|--------------|---------------------------------------|
| Setup        | Setup your CriblUtilities environment |
| Migrate      | Migrate database                      |
| Check        | Check file format adherence           |
| Check        | Check naming convention with regex    |

More information on [CLI-Docs](https://github.com/cinqict/CriblUtilities/blob/main/docs/cli-docs.md) documentation.

## 🛠 Pre requisites migrate use cases
- Create a local Cribl user. This user should minimally have the role: stream_editor.

## ⚠️ Disclaimer
This project is an independent initiative and is not affiliated, endorsed, or sponsored by Cribl. All trademarks and logos mentioned are the property of their respective owners. Please use this software responsibly and at your own risk.

## 📥 Usage
### PyPY
- brew install pipx
- pipx install cribl-utilities
- cribl-utilities --help
Link to package on [PyPI](https://pypi.org/project/cribl-utilities/).

## 💪 Development
- cd cribl-utilities
- 'pipx install -e .'

### Run example usage without installing the package
- Make sure to have installed a python version >=3.13, and have docker installed.
- `pip install -r requirements.txt`
- Example code without cli:
  - `cd cribl-utilities`
  - `docker compose up -d`
     - login and update admin password (default is `admin` and `admin`)
  - `python example_usage_without_cli.py`
  - Cleanup: `docker compose down`

### To serve the docs
- `mkdocs serve`

### To run unit tests
- `docker compose up -d`
- `pip install -r requirements.txt`
- `cd cribl-utilities`
- `pytest`
- Cleanup: `docker compose down`

### Typer (cli) related
##### Unix (macOS, Linux)
- `brew install pipx`
- `sudo pipx ensurepath --global` (this is to allow --global options)
- `pipx install poetry`
- `poetry config virtualenvs.in-project true` (this makes all venvs in the project)
##### Windows
-  Open PowerShell as administrator
- `pip install pipx`
- `pipx ensurepath` 
-  Close PowerShell and open a new one
- `pipx install poetry`
- `poetry config virtualenvs.in-project true` (this makes all venvs in the project)

### cribl-utilities CLI
- `poetry new cribl-utilities`
- `cd cribl-utilities`
- `poetry add typer`
- `poetry shell`
- `poetry build`
- `poetry install`
- `typer cribl_utilities.main utils docs --output docs/cli-docs.md --name cribl-utilities`

## 💻 Compilation of a new release
### Build and publish CLI
- make sure to have pipx and poetry installed and to be in the folder of the CLI itself
- `poetry shell`
- `poetry build`
- `poetry config http-basic.pypi <username> <password>` (run once)
- `poetry publish --build`
