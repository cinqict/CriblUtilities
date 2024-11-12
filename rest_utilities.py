import requests
import json
import os
from dotenv import load_dotenv, find_dotenv

_ = load_dotenv(find_dotenv())


def get_cribl_authentication_token(base_url: str = "http://localhost:19000") -> str:
    """Returns the auth token for the Cribl instance.

    Parameters
    ----------
    base_url : str
        The base URL of the Cribl instance.

    Returns
    -------
    str
        The auth token for the Cribl instance.

    """
    url = f"{base_url}/api/v1/auth/login"
    payload = json.dumps(
        {
            "username": os.environ["CRIBL_USERNAME"],
            "password": os.environ["CRIBL_PASSWORD"],
        }
    )
    headers = {"Content-Type": "application/json"}
    response = requests.request(method="POST", url=url, headers=headers, data=payload)
    if response.status_code != 200:
        raise Exception(f"Failed to get auth token. Response: {response.text}")
    return response.json()["token"]


def post_new_database_connection(
    base_url: str = "http://localhost:19000",
    payload: dict = {},
    cribl_authtoken: str = "",
    cribl_workergroup_name: str = "",
) -> dict:
    """Posts a new database connection to the Cribl instance.

    Parameters
    ----------
    base_url : str
        The base URL of the Cribl instance.
    cribl_authtoken : str
        The auth token for the Cribl instance.
    cribl_workergroup_name : str
        The name of the Cribl workergroup.

    Returns
    -------
    dict
        The response from the Cribl instance.

    """
    url = f"{base_url}/api/v1/m/{cribl_workergroup_name}/lib/database-connections"
    headers = {
        "Authorization": f"Bearer {cribl_authtoken}",
        "Content-Type": "application/json",
    }
    response = requests.request(method="POST", url=url, headers=headers, data=payload)
    if response.status_code != 200:
        return {
            "status": "error",
            "message": f"Failed to post new database connection. Response: {response.json()}",
        }
    return response.json()

def post_new_input(
    base_url: str = "http://localhost:19000",
    payload: dict = {},
    cribl_authtoken: str = "",
    cribl_workergroup_name: str = "",
) -> dict:
    """Posts a new input to the Cribl instance.

    Parameters
    ----------
    base_url : str
        The base URL of the Cribl instance.
    cribl_authtoken : str
        The auth token for the Cribl instance.
    cribl_workergroup_name : str
        The name of the Cribl workergroup.

    Returns
    -------
    dict
        The response from the Cribl instance.

    """
    url = f"{base_url}/api/v1/m/{cribl_workergroup_name}/lib/jobs"
    headers = {
        "Authorization": f"Bearer {cribl_authtoken}",
        "Content-Type": "application/json",
    }
    response = requests.request(method="POST", url=url, headers=headers, data=payload)
    if response.status_code != 200:
        return {
            "status": "error",
            "message": f"Failed to post new input. Response: {response.json()}",
        }
    return response.json()