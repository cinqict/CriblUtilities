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
import yaml
import re
import os
from dotenv import load_dotenv, find_dotenv
import logging
import traceback
from yamllint import linter
from yamllint.config import YamlLintConfig
import glob

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


def yaml_lint(cribl_config_folder: str) -> dict:
    """Checks if the YAML files in the Cribl config folder are valid.
    """

    def is_valid_yaml(path_file: str) -> bool:
        with open(path_file, 'r') as file:
            yaml_content = file.read()
        config_content = """
            extends: relaxed
            rules:
              # Disable all rules except basic syntax validation
              indentation: disable
              line-length: disable
              trailing-spaces: disable
              new-line-at-end-of-file: disable
              empty-lines: disable
              comments-indentation: disable
              comments: disable
              colons: disable
              document-start: disable
              hyphens: disable
              brackets: disable
            """
        config = YamlLintConfig(config_content)
        lint_result = linter.run(yaml_content, config)
        return not any(lint_result)  # Returns True if no linting errors

    def check_yaml_files_in_folder(base_path):
        yaml_files = glob.glob(os.path.join(base_path, 'groups', '*', 'local', '**', '*.yml'), recursive=True)
        valid_yaml = {}
        for yaml_file in yaml_files:
            valid_yaml[yaml_file] = is_valid_yaml(yaml_file)

        return valid_yaml

    results = check_yaml_files_in_folder(cribl_config_folder)
    return results



def regex_convention(cribl_config_folder: str, field: str, regex_pattern: str = None,
                     exceptions: list[str] = None) -> None:
    """Checks if the fields in the YAML files in the Cribl config folder match the regex pattern.

    Parameters
    ----------
    cribl_config_folder : str
        The path to the Cribl config folder.
    field : str
        The field to check. Supported fields are 'workergroup', 'sources', 'destinations', 'dataroutes', 'pipelines', and 'packs'.
    regex_pattern : str
        The regex pattern to match against the fields.
    exceptions : list[str]
        The fields to exclude from the check.

    """
    if field == 'workergroup':
        yaml_relative_path = 'local/cribl/groups.yml'
        full_paths = os.path.join(cribl_config_folder, yaml_relative_path)
        matching_paths = glob.glob(full_paths)
    elif field == 'sources':
        full_paths = os.path.join(cribl_config_folder, 'groups', '*', 'local', 'cribl', 'inputs.yml')
        matching_paths = glob.glob(full_paths)
        print("full paths ", matching_paths)
    elif field == 'destinations':
        full_paths = os.path.join(cribl_config_folder, 'groups', '*', 'local', 'cribl', 'outputs.yml')
        matching_paths = glob.glob(full_paths)
        print("full paths ", matching_paths)
    elif field == 'dataroutes':
        full_paths = os.path.join(cribl_config_folder, 'groups', '*', 'local', 'cribl', 'pipelines', 'route.yml')
        # Every name of routes
        matching_paths = glob.glob(full_paths)
        print("full paths ", matching_paths)
    elif field == 'pipelines':
        full_paths = os.path.join(cribl_config_folder, 'groups', '*', 'local', 'cribl', 'pipelines', '*')
        # name of the folder
        matching_paths = [yaml_full_path for yaml_full_path in glob.glob(full_paths) if os.path.isdir(yaml_full_path)]
        print("full paths ", matching_paths)
    elif field == 'packs':
        full_paths = os.path.join(cribl_config_folder, 'groups', '*', 'default', '*')
        # name of the folder
        matching_paths = [yaml_full_path for yaml_full_path in glob.glob(full_paths) if os.path.isdir(yaml_full_path)]
        print("full paths ", matching_paths)
    else:
        raise ValueError("Field not supported")

    def open_yaml(yaml_full_path):
        try:
            with open(yaml_full_path, 'r') as file:
                data_file = yaml.safe_load(file)
            return data_file
        except FileNotFoundError:
            print(f"Error: File not found at {yaml_full_path}")
            return
        except yaml.YAMLError as e:
            print(f"Error parsing YAML file: {e}")
            return
    data = []
    for yaml_full_path in matching_paths:
        print('File/folder: ', yaml_full_path)
        # Read the YAML file or the foldernames
        if field == 'workergroup':
            data.append(list(open_yaml(yaml_full_path).keys()))
        if field == 'sources' and 'inputs' in open_yaml(yaml_full_path):
            data.append(list(open_yaml(yaml_full_path)['inputs'].keys()))
        elif field == 'destinations' and 'outputs' in open_yaml(yaml_full_path):
            data.append(list(open_yaml(yaml_full_path)['outputs'].keys()))
        elif field == 'dataroutes' and 'routes' in open_yaml(yaml_full_path):
            data.append([route['name'] for route in open_yaml(yaml_full_path)['routes']])
        elif field == 'pipelines':
            #name of the folder
            data.append(os.path.basename(yaml_full_path))
        elif field == 'packs':
            #name of the folder
            data.append(os.path.basename(yaml_full_path))

    #if field == 'pipelines' or field == 'packs':
    data = [item for sublist in data for item in (sublist if isinstance(sublist, list) else [sublist])]
    # Filter out the fields to be excluded
    excluded_fields = exceptions[0].replace(' ','').split(',') if exceptions else []
    print('excluded_fields', excluded_fields)
    print('data', data)
    filtered_fields = [field for field in data if field not in excluded_fields]
    print('filtered_fields', filtered_fields)

    # Validate fields against the regex
    if not regex_pattern:
        print("No regex pattern provided.")
        return
    for field in filtered_fields:
        if re.match(regex_pattern, field):
            print(f"'{field}' matches the pattern.")
        else:
            print(f"'{field}' does NOT match the pattern.")

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
