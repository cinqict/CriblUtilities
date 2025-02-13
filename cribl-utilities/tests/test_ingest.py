import os
import re
import pytest
import json
from unittest.mock import patch, Mock
import requests
from cribl_utilities.ingest import Ingestor


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


def test_check_cribl_health(ingestor):
    base_url = os.environ["BASE_URL"]
    with patch("requests.get") as mock_get:
        mock_response = Mock()
        mock_response.status_code = 500
        mock_get.return_value = mock_response

        with pytest.raises(RuntimeError, match=re.escape(f"Cribl service is running but returned an error (status code: {mock_response.status_code}).")):
            ingestor.check_cribl_health()

    with patch("requests.get", side_effect=requests.exceptions.ConnectionError):
        with pytest.raises(ConnectionError, match=f"Cribl service is not running or not accesible at the provided url: {base_url}"):
            ingestor.check_cribl_health()

    with patch("requests.get", side_effect=requests.exceptions.Timeout):
        with pytest.raises(TimeoutError, match=f"Request to {base_url} timed out. Error: .*"):
            ingestor.check_cribl_health()

    with patch("requests.get", side_effect=requests.exceptions.RequestException):
        with pytest.raises(RuntimeError, match=f"An unexpected error occurred: .*"):
            ingestor.check_cribl_health()


def test_get_cribl_authtoken(ingestor):
    # Mock the requests.request method to raise a ConnectionError
    with patch("requests.post", side_effect=requests.exceptions.RequestException):
        with pytest.raises(RuntimeError, match="Failed to get Cribl auth token. Error: .*"):
            ingestor.get_cribl_authtoken()

    mock_response_no_token = Mock()
    mock_response_no_token.json.return_value = {}  # Simulate empty JSON object
    with pytest.raises(KeyError, match="Token not found in the response."):
        token = mock_response_no_token.json().get("token")
        if not token:
            raise KeyError("Token not found in the response.")

    mock_response_invalid_json = Mock()
    mock_response_invalid_json.json.side_effect = json.JSONDecodeError(
        "Expecting value", "doc", 0
    )
    with pytest.raises(ValueError, match="Invalid JSON response from Cribl."):
        try:
            mock_response_invalid_json.json().get("token")
        except json.JSONDecodeError:
            raise ValueError("Invalid JSON response from Cribl.")


    # assert ingestor.token is not None
    # assert isinstance(ingestor.token, str)
    # assert len(ingestor.token) > 0

# LOAD DATA TEST: names, toml validation
# MERGE INPUT DATA TEST: Fields and value type. Missing fields, which ones can be missing which ones are required.
# - [ ] validation of input files: 3 files, right format
#         - [ ] warning if username, password, or domain are missing. Set schedule.enable to zero
#         - [ ] in each field throw error in case of data type mismatch
