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

_ = load_dotenv(find_dotenv())


def get_cribl_authentication_token(base_url: str = os.environ["BASE_URL"]) -> str:
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
    base_url: str = os.environ["BASE_URL"],
    payload: dict = {},
    cribl_authtoken: str = "",
    cribl_workergroup_name: str = os.environ["CRIBL_WORKERGROUP_NAME"],
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
    base_url: str = os.environ["BASE_URL"],
    payload: dict = {},
    cribl_authtoken: str = "",
    cribl_workergroup_name: str = os.environ["CRIBL_WORKERGROUP_NAME"],
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