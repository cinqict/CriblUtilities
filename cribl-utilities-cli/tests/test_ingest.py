import pytest
from cribl_utilities_cli.ingest import Ingestor
import sys

@pytest.fixture
def ingestor():
    return Ingestor()


def test_check_docker_running_connection_error():
    ingestor = Ingestor()
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
