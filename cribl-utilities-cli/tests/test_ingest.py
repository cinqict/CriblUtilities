import os
import pytest
from cribl_utilities_cli.ingest import Ingestor
import sys

@pytest.fixture
def ingestor():
    return Ingestor()


def test_environment_variables(ingestor, monkeypatch):
    mandatory_vars = {
        "CRIBL_USERNAME": "your_cribl_username",
        "CRIBL_PASSWORD": "your_cribl_password",
        "BASE_URL": "your_base_url",
        "CRIBL_WORKERGROUP_NAME": "your_workergroup_name"
    }

    # Store original environment variables
    valid_vars = {var: os.environ.get(var) for var in mandatory_vars.keys()}

    # Helper function to reset all environment variables to valid values
    def reset_env():
        for key, value in valid_vars.items():
            monkeypatch.setenv(key, value)

    for var, default_value in mandatory_vars.items():
        # Test missing variable
        reset_env()
        monkeypatch.delenv(var, raising=False)
        print(f"Testing 1 {var}: os.environ state -> {os.environ.get(var)}")
        with pytest.raises(EnvironmentError, match=f"Environment variable {var} is not set."):
            ingestor.check_environment_variables()

        # Test empty variable
        reset_env()
        monkeypatch.setenv(var, "")
        print(f"Testing 2 {var}: os.environ state -> {os.environ[var]}")
        with pytest.raises(ValueError, match=f"Mandatory environment variable {var} is empty."):
            ingestor.check_environment_variables()

        # Test default placeholder value
        reset_env()
        monkeypatch.setenv(var, default_value)
        print(f"Testing 3 {var}: os.environ state -> {os.environ[var]}")
        with pytest.raises(ValueError, match=f"Mandatory environment variable {var} is not set correctly."):
            ingestor.check_environment_variables()


def test_check_docker_running_connection_error(ingestor):
    try:
        ingestor.check_docker_running()
    except RuntimeError as e:
        sys.exit(e)

def test_get_cribl_authtoken(ingestor):
    # check self.token, what to check about the token?
    ingestor.get_cribl_authtoken()
    assert ingestor.token is not None
    assert isinstance(ingestor.token, str)
    assert len(ingestor.token) > 0

# LOAD DATA TEST: names, toml validation
# MERGE INPUT DATA TEST: Fields and value type. Missing fields, which ones can be missing which ones are required.
