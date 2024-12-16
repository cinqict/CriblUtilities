#
#           .:-=====-:.         ---   :--:            .--:           .--====-:.                
#     :=*####***####*+:     :###.  =###*.          -##*        -+#####**####*=:             
#   .*##*=:.     .:=*#=     :###.  =#####-         -##*      =###+-.      :=*##*:           
#  -###-                    :###.  =##++##+        -##*    .*##+.            -###=          
# :###:                     :###.  =##+ +##*.      -##*    *##=               .*##=         
# *##=                      :###.  =##+  -###-     -##*   =##*                 -###         
# ###-                      :###.  =##+   .*##+    -##*   +##+                 .###.        
# ###=                      :###.  =##+     =##*.  -##*   =##*           :     :###.        
# =##*.                     :###.  =##+      :*##- -##*   .###-         ---:.  *##+         
#  +##*.                    :###.  =##+       .*##+-##*    -###-         .----=##*          
#   =###+:         .-**.    :###.  =##+         =##*##*     :*##*-         -=--==       ... 
#    .=####+==-==+*###+:    :###.  =##+          :*###*       -*###*+=-==+###+----.    ----:
#       :=+*####**+=:       .***   =**=            +**+         .-=+*####*+=:  .:-.    .---.
#                                                                                           
#                                                                                          
#   Copyright 2024 CINQ ICT b.v.
#
#   Licensed under the Apache License, Version 2.0 (the "License");
#   you may not use this file except in compliance with the License.
#   You may obtain a copy of the License at
#
#       http://www.apache.org/licenses/LICENSE-2.0
#
#   Unless required by applicable law or agreed to in writing, software
#   distributed under the License is distributed on an "AS IS" BASIS,
#   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#   See the License for the specific language governing permissions and
#   limitations under the License.

import requests
import json
import os
from dotenv import load_dotenv, find_dotenv
import logging
import traceback

_ = load_dotenv(find_dotenv())


def environment_variables() -> None:
    """Checks if the required environment variables are set."""
    mandatory_vars = {
        "CRIBL_USERNAME": "your_cribl_username",
        "CRIBL_PASSWORD": "your_cribl_password",
        "BASE_URL": "your_base_url",
        "CRIBL_WORKERGROUP_NAME": "your_workergroup_name"
    }

    for var, default_value in mandatory_vars.items():
        if var not in os.environ:
            raise EnvironmentError(f"Environment variable {var} is not set.")
        if os.environ[var] == "":
            raise ValueError(f"Mandatory environment variable {var} is empty.")
        if os.environ[var] == default_value:
            raise ValueError(f"Mandatory environment variable {var} is not set correctly.")


def cribl_health(base_url: str = os.environ["BASE_URL"]) -> str:
    """Checks if Cribl is accessible."""
    try:
        response = requests.get(base_url)
        if response.status_code != 200:
            raise RuntimeError(f"Cribl service is running but returned an error (status code: {response.status_code}).")
        return "Cribl service is running and healthy."
    except requests.exceptions.ConnectionError:
        logging.error("Connection error occurred:\n" + traceback.format_exc())
        raise ConnectionError(
            f"Cribl service is not running or not accesible at the provided url: {base_url}"
        )
    except requests.exceptions.Timeout as e:
        raise TimeoutError(f"Request to {base_url} timed out. Error: {e}")
    except requests.exceptions.RequestException as e:
        raise RuntimeError(f"An unexpected error occurred: {e}")



def get_cribl_authentication_token(base_url: str = os.getenv("BASE_URL", "http://localhost:19000")) -> str:
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
            "username": os.getenv("CRIBL_USERNAME", "admin"),
            "password": os.getenv("CRIBL_PASSWORD", "admin"),
        }
    )
    headers = {"Content-Type": "application/json"}
    # try:
    #     response = requests.request(method="POST", url=url, headers=headers, data=payload)
    # except requests.exceptions.RequestException as e:
    #     raise ConnectionError(f"Failed to get Cribl auth token. Error: {e}")

    try:
        response = requests.post(url, headers=headers, data=payload)
    except requests.exceptions.RequestException as e:
        raise RuntimeError(f"Failed to get Cribl auth token. Error: {e}")

    try:
        token = response.json().get("token")
        if not token:
            raise KeyError("Token not found in the response.")
    except json.JSONDecodeError:
        raise ValueError("Invalid JSON response from Cribl.")

    return token


def post_new_database_connection(
    base_url: str = os.getenv("BASE_URL", "http://localhost:19000"),
    payload: dict = None,
    cribl_authtoken: str = "",
    cribl_workergroup_name: str = os.getenv("CRIBL_WORKERGROUP_NAME", "default"),
) -> dict:
    """Posts a new database connection to the Cribl instance.

    Parameters
    ----------
    base_url : str
        The base URL of the Cribl instance.
    payload : dict
        The payload to post to the Cribl instance.
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
    data_sent = json.dumps(payload)
    response = requests.request(method="POST", url=url, headers=headers, data=data_sent)
    if response.status_code != 200:
        return {
            "status": "error",
            "message": f"Failed to post new database connection. Response: {response.text}",
        }
    return response.json()


def post_new_input(
    base_url: str = os.getenv("BASE_URL", "http://localhost:19000"),
    payload: dict = None,
    cribl_authtoken: str = "",
    cribl_workergroup_name: str = os.getenv("CRIBL_WORKERGROUP_NAME", "default"),
) -> dict:
    """Posts a new input to the Cribl instance.

    Parameters
    ----------
    base_url : str
        The base URL of the Cribl instance.
    payload : dict
        The payload to post to the Cribl instance.
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
            "message": f"Failed to post new input. Response: {response.text}",
        }
    return response.json()
