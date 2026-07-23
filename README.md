# 🚀 CriblUtilities

CriblUtilities is a Python CLI package that streamlines migration to Cribl Stream and validates configurations. With minimal setup, it transfers configurations from existing tools to Cribl Stream. It also integrates with Cribl GitOps workflows to verify naming conventions and file formats before implementing changes.

**Contents:** [Functionality](#-functionality) · [Disclaimer](#-disclaimer) · [Usage](#-usage) · [Prerequisites](#-prerequisites) · [Development](#-development) · [Releasing](#-releasing)

## 🫶 Functionality

| **Command** | **Explanation**                       |
|-------------|----------------------------------------|
| `setup`     | Set up your CriblUtilities environment |
| `migrate`   | Migrate database                       |
| `check`     | Check file format adherence            |
| `check`     | Check naming convention with regex     |

See the full [CLI docs](https://github.com/cinqict/CriblUtilities/blob/main/docs/cli-docs.md) for every command and option.

## ⚠️ Disclaimer

This project is an independent initiative and is not affiliated, endorsed, or sponsored by Cribl. All trademarks and logos mentioned are the property of their respective owners. Please use this software responsibly and at your own risk.

## 📥 Usage

Install the CLI from PyPI:

```shell
brew install pipx
pipx install cribl-utilities
cribl-utilities --help
```

Package page: [PyPI](https://pypi.org/project/cribl-utilities/).

## 🛠 Prerequisites

- A local Cribl user with, at minimum, the `stream_editor` role — required for the migrate use cases.

## 💪 Development

### Requirements

- Python **>=3.13**
- Docker
- [pipx](https://pipx.pypa.io/) and [Poetry](https://python-poetry.org/)

### Install the CLI toolchain

<details>
<summary>macOS / Linux</summary>

```shell
brew install pipx
sudo pipx ensurepath --global  # allows the --global option below
pipx install poetry
poetry config virtualenvs.in-project true  # keep venvs inside the project
```
</details>

<details>
<summary>Windows (PowerShell, run as administrator)</summary>

```powershell
pip install pipx
pipx ensurepath
# close and reopen PowerShell
pipx install poetry
poetry config virtualenvs.in-project true  # keep venvs inside the project
```
</details>

### Work on the CLI package

```shell
cd cribl-utilities
pipx install -e .
```

### Run the example script without installing the CLI

```shell
pip install -r requirements.txt
cd cribl-utilities
docker compose up -d
# log in and update the admin password (default is admin / admin)
python example_usage_without_cli.py
docker compose down  # cleanup
```

### Run the unit tests

```shell
docker compose up -d
pip install -r requirements.txt
cd cribl-utilities
pytest
docker compose down  # cleanup
```

### Serve the docs locally

```shell
mkdocs serve
```

<details>
<summary>Reference: how the CLI project was originally scaffolded</summary>

These commands are not needed for day-to-day development — they document how the `cribl-utilities` Poetry/Typer project was first created.

```shell
poetry new cribl-utilities
cd cribl-utilities
poetry add typer
poetry shell
poetry build
poetry install
typer cribl_utilities.main utils docs --output docs/cli-docs.md --name cribl-utilities
```
</details>

## 💻 Releasing

Build and publish a new CLI release from the `cribl-utilities` folder:

```shell
poetry shell
poetry build
poetry config http-basic.pypi <username> <password>  # run once
poetry publish --build
```
