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

import json
import re
import os
from uuid import uuid4
from typing import List

import tomli
from pydantic import BaseModel

from cribl_utilities_cli.rest_utilities import (
    environment_variables,
    cribl_health,
    get_cribl_authentication_token,
    post_new_database_connection,
    post_new_input,
)
from cribl_utilities_cli.schemas import (
    InputSchema,
    Metadata,
    Schedule,
    Collector,
    CollectorConf,
    Run,
    InputType,
    ConnectionSchema,
)


def load_examples(files: List[str]) -> tuple[dict, dict]:
    """
    Load and parse two TOML files, returning the contents as dictionaries.

    Parameters
    ----------
    files : list
        A list containing two file paths to TOML files.

    Returns
    -------
    dict
        A tuple containing two dictionaries with the parsed data from each TOML file.
    """

    def load_and_format(file_path: str) -> dict:
        file_name = os.path.basename(file_path)
        folder_path = os.path.dirname(file_path)
        folder_name = os.path.basename(folder_path)

        if not os.path.exists(folder_path):
            raise NotADirectoryError(
                f"Folder not found: {folder_name}. Make sure the folder '{folder_name}' exists."
            )
        elif not os.path.exists(file_path):
            raise FileNotFoundError(f"File not found: {file_name}. "
                                    f"Make sure {file_name} exists and it is in {folder_name} folder.")

        with open(file_path) as f:
            tmp = f.read()
            tmp = re.sub(r"\\\n", " ", tmp)
            tmp_formatted = re.sub(r"(\s*=\s*)(.*)", r"\1'''\2'''", tmp)
            tomli_db_inputs = dict(tomli.loads(tmp_formatted).items())

        return tomli_db_inputs

    # Load and parse each file
    dict_items1 = load_and_format(files[0])
    dict_items2 = load_and_format(files[1])

    return dict_items1, dict_items2


def is_cron_format(value: str) -> bool:
    """
    Check if the given value is in a valid cron schedule format.

    Parameters
    ----------
    value : str
        The value to check.

    Returns
    -------
    bool
        True if the value is a valid cron schedule format, False otherwise.
    """
    if value.isdigit():
        return False

    # Cron schedule regex: Matches standard cron patterns
    cron_regex = (
        r"^(\*|([0-5]?\d)) (\*|([01]?\d|2[0-3])) (\*|([0-2]?\d)) (\*|([1-7]))$|"
        r"^@(?:yearly|annually|monthly|weekly|daily|hourly)$"
    )

    return bool(re.match(cron_regex, value.strip()))


class Ingestor:
    def __init__(
        self,
        examples_folder: str = "examples",
    ):
        self.examples_folder = examples_folder
        self.identities = None
        self.token = None
        self.connection = None
        self.input = None

    def __str__(self):
        return f"Authentication: {self.identities}\nConnection: {self.connection}\nInput: {self.input}"

    def check_environment_variables(self) -> None:
        return environment_variables()

    def check_cribl_health(self, base_url: str = os.getenv("BASE_URL", "http://localhost:19000")) -> str:
        return cribl_health(base_url=base_url)

    def get_cribl_authtoken(self, base_url: str = os.getenv("BASE_URL", "http://localhost:19000")) -> None:
        self.token = get_cribl_authentication_token(base_url=base_url)

    def merge_examples_input(self, file_names: list | None = None) -> dict:
        """

        Parameters
        ----------
        file_names : list
            A list containing two file names to be merged. The first file should contain the input data,
            and the second file should contain the connection data.

        Returns
        -------
        dict
            A dictionary containing the merged data from the two files.

        """

        if file_names and file_names[0]:
            path1 = f"{self.examples_folder}/{file_names[0]}"
        else:
            path1 = f"{self.examples_folder}/db_inputs.conf"
        if file_names and file_names[1]:
            path2 = f"{self.examples_folder}/{file_names[1]}"
        else:
            path2 = f"{self.examples_folder}/db_connections.conf"

        paths = [path1, path2]

        tomli_db_inputs, tomli_db_connections = load_examples(files=paths)

        merged_data = {}
        dict_db_inputs = dict(tomli_db_inputs)
        dict_db_connections = dict(tomli_db_connections)

        for key, input_value in dict_db_inputs.items():
            connection_key = input_value.get("connection")
            connection_data = dict_db_connections.get(connection_key, {})
            merged_data[key] = {**input_value, **connection_data}

        def transform_disabled_values(data: dict):
            """
            Transform values in "disabled" entry according to provided table in Mapping API Cribl
            """
            for trans_key, trans_sub_dict in data.items():
                if "disabled" in trans_sub_dict:
                    value = trans_sub_dict["disabled"]
                    if isinstance(value, str):
                        value = value.lower()
                    if value in ["true", 1, True, "1"]:
                        trans_sub_dict["disabled"] = False
                    elif value in ["false", 0, False, "0"]:
                        trans_sub_dict["disabled"] = True
            return data

        def seconds_to_cron(seconds: int) -> str:
            """
            Transforms a given time in seconds to a cron schedule.

            Parameters
            ----------
            seconds : int
                The time in seconds to be converted to a cron schedule.

            Returns
            -------
            str
                The cron schedule expression.
            """
            if seconds < 60:
                return f"*/{seconds} * * * *"
            elif seconds < 3600:
                minutes = seconds // 60
                return f"*/{minutes} * * * *"
            elif seconds < 86400:
                hours = seconds // 3600
                return f"0 */{hours} * * *"
            else:
                days = seconds // 86400
                return f"0 0 */{days} * *"

        merged_input_data = transform_disabled_values(merged_data)

        for key, sub_dict in merged_input_data.items():
            interval = sub_dict.get("interval")
            if interval and not is_cron_format(interval):
                try:
                    sub_dict["interval"] = seconds_to_cron(int(interval))
                except ValueError:
                    continue

        return merged_input_data

    def load_input(self, file_names: list | None = None) -> list[BaseModel] | None:
        """
        Load the input examples from the TOML files and create InputSchema instances.

        Parameters
        ----------
        file_names: list
            A list containing two file names to be merged. The first file should contain the input data,
            and the second file should contain the connection data.

        Returns
        -------
        List[InputSchema]
            A list containing the InputSchema instances.

        """

        def create_metadata(data):
            """
            Create a list of Metadata instances from the given data.

            Parameters
            ----------
            data

            Returns
            -------


            """
            return [
                Metadata(name="host", value=data.get("host", "")),
                Metadata(name="index", value=data.get("index", "")),
                Metadata(name="source", value=data.get("source", "")),
                Metadata(name="sourcetype", value=data.get("sourcetype", "")),
            ]

        merged_data = self.merge_examples_input(file_names)
        # Parsing tomli_input to create InputSchema instances
        input_obj = [
            InputSchema(
                schedule=Schedule(
                    interval=row["interval"],
                    run=Run(mode=row["mode"]),
                    disabled=row["disabled"],
                ),
                collector=Collector(
                    conf=CollectorConf(connection=row["connection"], query=row["query"])
                ),
                input=InputType(metadata=create_metadata(row)),
                id=(
                    f"{os.getenv('DBCOLL_PREFIX', '') + '-' if os.getenv('DBCOLL_PREFIX', '') else ''}"
                    f"{key}-"
                    f"{uuid4() if os.getenv('DBCOLL_SUFFIX', '') == '{guid}' else os.getenv('DBCOLL_SUFFIX', '')}"
                ),
            )
            for key, row in merged_data.items()
        ]

        def transform_to_js_expression(query: str) -> str:
            """
            Transforms the SQL query strings into a valid JavaScript expression
            for Cribl, enclosed in backticks.
            """
            # Escape double quotes for JavaScript compatibility
            escaped_query = query.replace('"', '\\"')
            # Wrap the query in backticks
            js_expression = f"`{escaped_query}`"
            return js_expression

        for i in input_obj:
            i.collector.conf.query = transform_to_js_expression(i.collector.conf.query)

        self.input = input_obj

        return self.input

    def post_db_inputs(
        self,
        base_url: str = os.getenv("BASE_URL", "http://localhost:19000"),
        cribl_workergroup_name: str = os.getenv("CRIBL_WORKERGROUP_NAME", "default"),
    ) -> list[dict]:
        return [
            post_new_input(
                base_url=base_url,
                cribl_authtoken=self.token,
                cribl_workergroup_name=cribl_workergroup_name,
                payload=i.model_dump_json(),
            )
            for i in self.input
        ]

    def merge_examples_connections(self, file_names: list | None = None) -> dict:
        """
        Merge the examples files containing the identities and connections data.
        Parameters
        ----------
        file_names : list
            A list containing two file names to be merged. The first file should contain the identities data,
            and the second file should contain the connections' data.

        Returns
        -------
        merged_connections_data : dict
            A dictionary containing the merged data from the two files.
        """
        if file_names and file_names[0]:
            path1 = f"{self.examples_folder}/{file_names[0]}"
        else:
            path1 = f"{self.examples_folder}/identities.conf"
        if file_names and file_names[1]:
            path2 = f"{self.examples_folder}/{file_names[1]}"
        else:
            path2 = f"{self.examples_folder}/db_connections.conf"

        paths = [path1, path2]

        tomli_db_identities, tomli_db_connections = load_examples(files=paths)

        merged_data = {}
        dict_db_identities = dict(tomli_db_identities)
        dict_db_connections = dict(tomli_db_connections)

        for key, input_value in dict_db_connections.items():
            identity_key = input_value.get("identity")
            identity_data = dict_db_identities.get(identity_key, {})
            merged_data[key] = {**input_value, **identity_data}

        def cribl_connectionstring_configobj(data: dict) -> dict:
            """
            Transform the connection data to include a properly formatted `configObj` or `customizedJdbcUrl`.

            This function processes the merged connection data and updates each entry based on its connection type.
            For connections of type 'mssql_jtds_win_auth', it creates a `configObj` dictionary with the necessary
            authentication and connection options. For other connection types, it constructs a `customizedJdbcUrl`
            if it does not already exist.

            Parameters
            ----------
            data : dict
                The dictionary containing the merged connection data.

            Returns
            -------
            dict
                The updated dictionary with `configObj` or `customizedJdbcUrl` added to each connection entry.
            """
            for conn_key, conn_sub_dict in data.items():
                if conn_sub_dict["connection_type"] == "mssql_jtds_win_auth":
                    configobj = {
                        "authentication": {
                            "type": "ntlm",
                            "options": {
                                "userName": conn_sub_dict["username"],
                                "password": conn_sub_dict["password"],
                                "domain": conn_sub_dict.get("domain_name", ""),
                            },
                        },
                        "options": {
                            "connectTimeout": 15000,
                            "trustServerCertificate": True,
                        },
                        "connectionTimeout": 15000,
                        "port": conn_sub_dict["port"],
                        "server": (
                            f"{os.getenv('BASE_URL', 'http://localhost:19000')}/api/v1/m/"
                            f"{os.getenv('CRIBL_WORKERGROUP_NAME', 'default')}/lib/database-connections"
                        ),
                        "database": conn_sub_dict.get("database", ""),
                    }
                    conn_sub_dict["configObj"] = configobj
                    conn_sub_dict.pop("customizedJdbcUrl", None)
                else:
                    if "customizedJdbcUrl" not in conn_sub_dict:
                        connection_type = conn_sub_dict.get("connection_type", "")
                        host = conn_sub_dict.get("host", "")
                        port = conn_sub_dict.get("port", "")
                        jdbc_use_ssl = conn_sub_dict.get("jdbcUseSSL", "")
                        username = conn_sub_dict.get("username", "")
                        password = conn_sub_dict.get("password", "")
                        conn_sub_dict["customizedJdbcUrl"] = (
                            f"jdbc:{connection_type}://{host}:{port};"
                            f"encrypt={jdbc_use_ssl};user={username};password={password};"
                        )
            return data

        def auth_type(data: dict) -> dict:
            # If connection_type = mssql_jdts_win_auth fill this with configObj
            # else fill with connectionString.
            for auth_key, auth_sub_dict in data.items():
                if auth_sub_dict["connection_type"] == "mssql_jtds_win_auth":
                    auth_sub_dict["authType"] = "configObj"
                else:
                    auth_sub_dict["authType"] = "connectionString"

            return data

        def cribl_database_type(data: dict) -> dict:
            """
            Transform the values of the 'connection_type' key in the merged_data dictionary.

            Parameters
            ----------
            data : dict
                The dictionary containing the merged data with 'connection_type' keys.

            Returns
            -------
            dict
                The transformed dictionary with updated 'connection_type' values.
            """
            connection_type_mapping = {
                "oracle_service": "oracle",
                "oracle": "oracle",
                "mssql_jtds_win_auth": "sqlserver",
                "generic_mssql": "sqlserver",
                "db2": None,  # '-not supported yet-',
                "postgres": "postgres",
                "sybase_ase": None,  # '-not supported yet-',
                "vertica": None,  # '-not supported yet-'
            }

            for cribl_key, cribl_sub_dict in data.items():
                if "connection_type" in cribl_sub_dict:
                    original_type = cribl_sub_dict["connection_type"]
                    cribl_sub_dict["connection_type"] = connection_type_mapping.get(
                        original_type, original_type
                    )

            return data

        merged_connections_data = cribl_connectionstring_configobj(merged_data)
        merged_connections_data = auth_type(merged_connections_data)
        merged_connections_data = cribl_database_type(merged_connections_data)

        return merged_connections_data

    def load_connections(
        self, file_names: list | None = None
    ) -> list[BaseModel] | None:
        """
        Load the connection examples from the TOML files and create ConnectionSchema instances.

        This method merges the identities and connections data from the specified TOML files,
        transforms the data as needed, and creates instances of the ConnectionSchema class.

        Parameters
        ----------
        file_names : list, optional
            A list containing two file names to be merged. The first file should contain the identities data,
            and the second file should contain the connections' data. If not provided, default file names are used.

        Returns
        -------
        list[BaseModel] | None
            A list containing the ConnectionSchema instances, or None if no connections are loaded.
        """
        merged_data = self.merge_examples_connections(file_names)
        connections_obj = []

        for key, row in merged_data.items():
            connection_data = {
                "id": (
                    f"{os.getenv('DBCONN_PREFIX', '') + '-' if os.getenv('DBCONN_PREFIX', '') else ''}"
                    f"{key}-{uuid4() if os.getenv('DBCONN_SUFFIX', '') == '{guid}' else os.getenv('DBCONN_SUFFIX', '')}"
                ),
                "databaseType": row.get("connection_type"),
                "username": row.get("username"),
                "password": row.get("password"),
                "database": row.get("database"),
                "disabled": row.get("disabled"),
                "host": row.get("host"),
                "identity": row.get("identity"),
                "jdbcUseSSL": row.get("jdbcUseSSL"),
                "localTimezoneConversionEnabled": row.get(
                    "localTimezoneConversionEnabled"
                ),
                "port": row.get("port"),
                "readonly": row.get("readonly"),
                "timezone": row.get("timezone"),
                "authType": row.get("authType"),
            }
            if "configObj" in row:
                connection_data["configObj"] = row.get("configObj")
            if "customizedJdbcUrl" in row:
                connection_data["connectionString"] = row.get("customizedJdbcUrl")
            #print("CONNECTION DATA :", connection_data)
            connections_obj.append(ConnectionSchema(**connection_data))

        self.connection = connections_obj

        return self.connection

    def post_db_connections(
        self,
        base_url: str = os.getenv("BASE_URL", "http://localhost:19000"),
        cribl_workergroup_name: str = os.getenv("CRIBL_WORKERGROUP_NAME", "default"),
    ) -> list[dict]:
        responses = []
        for i in self.connection:
            payload = json.loads(i.model_dump_json())
            if "configObj" in payload:
                payload["configObj"] = json.dumps(
                    payload["configObj"]
                )  # Convert configObj to JSON string
            response = post_new_database_connection(
                base_url=base_url,
                cribl_authtoken=self.token,
                cribl_workergroup_name=cribl_workergroup_name,
                payload=payload,
            )
            responses.append(response)

        return responses
