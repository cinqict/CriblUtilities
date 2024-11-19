import re
from uuid import uuid4
from typing import List

import tomli
from pydantic import BaseModel

from rest_utilities import get_cribl_authentication_token, post_new_database_connection, post_new_input
from schemas import InputSchema, Metadata, Schedule, Collector, CollectorConf, Run, InputType, ConnectionSchema


def load_examples(files: List[str]) -> tuple[object, object]:
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

    def load_and_format(file_path: str) -> object:
        with open(file_path) as f:
            tmp = f.read()
            tmp = re.sub(r"\\\n", " ", tmp)
            tmp_formatted = re.sub(r"(\s*=\s*)(.*)", r"\1'''\2'''", tmp)
            tomli_db_inputs = tomli.loads(tmp_formatted).items()
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
    cron_regex = r'^(\*|([0-5]?\d)) (\*|([01]?\d|2[0-3])) (\*|([0-2]?\d)) (\*|([1-7]))$|^@(?:yearly|annually|monthly|weekly|daily|hourly)$'

    return bool(re.match(cron_regex, value.strip()))


class Ingestor:
    def __init__(
            self,
            examples_folder: str = "examples",
    ):
        self.examples_folder = examples_folder
        self.identities = None
        self.connection = None
        self.input = None

    def __str__(self):
        return f"Authentication: {self.identities}\nConnection: {self.connection}\nInput: {self.input}"

    def get_cribl_authtoken(self, base_url: str = "http://localhost:19000") -> None:
        self.token = get_cribl_authentication_token(base_url=base_url)

    def merge_examples_input(self, file_names: list | None = None) -> object:
        """

        Parameters
        ----------
        file_names : list
            A list containing two file names to be merged. The first file should contain the input data, and the second file should contain the connection data.

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
            for key, sub_dict in data.items():
                if 'disabled' in sub_dict:
                    value = sub_dict['disabled']
                    if isinstance(value, str):
                        value = value.lower()
                    if value in ['true', 1, True, '1']:
                        sub_dict['disabled'] = False
                    elif value in ['false', 0, False, '0']:
                        sub_dict['disabled'] = True
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

        merged_input_data = transform_disabled_values(merged_data).items()

        for key, sub_dict in merged_input_data:
            interval = sub_dict.get('interval')
            if interval and not is_cron_format(interval):
                try:
                    sub_dict['interval'] = seconds_to_cron(int(interval))
                except ValueError:
                    continue

        return merged_input_data

    def load_input(self, file_names: list | None = None) -> list[BaseModel] | None:
        """
        Load the input examples from the TOML files and create InputSchema instances.

        Parameters
        ----------
        file_names: list
            A list containing two file names to be merged. The first file should contain the input data, and the second file should contain the connection data.

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
                Metadata(name="host", value=data.get("host","")),
                Metadata(name="index", value=data.get("index","")),
                Metadata(name="source", value=data.get("source", "")),
                Metadata(name="sourcetype", value=data.get("sourcetype",""))
            ]

        merged_data = self.merge_examples_input(file_names)
        # Parsing tomli_input to create InputSchema instances
        input_obj = [
            InputSchema(
                schedule=Schedule(
                    interval=row['interval'],
                    run=Run(mode=row['mode']),
                    disabled=row['disabled']
                ),
                collector=Collector(
                    conf=CollectorConf(
                        connection=row['connection'],
                        query=row['query']
                    )
                ),
                input=InputType(
                    metadata=create_metadata(row)
                ),
                id=f"{key}-{uuid4()}"
            )
            for key, row in merged_data
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
            base_url: str = "http://localhost:19000",
            cribl_workergroup_name: str = "default",
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

    def merge_examples_connections(self, file_names: list | None = None) -> object:
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

        def cribl_databaseType(merged_data: dict) -> dict:
            """
            Transform the values of the 'connection_type' key in the merged_data dictionary.

            Parameters
            ----------
            merged_data : dict
                The dictionary containing the merged data with 'connection_type' keys.

            Returns
            -------
            dict
                The transformed dictionary with updated 'connection_type' values.
            """
            connection_type_mapping = {
                'oracle_service': 'oracle',
                'oracle': 'oracle',
                'mssql_jtds_win_auth': 'sqlserver',
                'generic_mssql': 'sqlserver',
                'db2': '-not supported yet-',
                'postgres': 'postgres',
                'sybase_ase': '-not supported yet-',
                'vertica': '-not supported yet-'
            }

            for key, sub_dict in merged_data.items():
                if 'connection_type' in sub_dict:
                    original_type = sub_dict['connection_type']
                    sub_dict['connection_type'] = connection_type_mapping.get(original_type, original_type)

            return merged_data

        def cribl_connectionString(merged_data: dict) -> dict:
            """
            Transform the values of the 'customizedJdbcUrl' key in the merged_data dictionary.
            If not available, this needs to be drafted using parameters (in curly brackets) available:
            jdbc:{connection_type}://{host}:{port};encrypt={jdbcUseSSL};user={username};password={password};

            Parameters
            ----------
            merged_data : dict
                The dictionary containing the merged data with 'customizedJdbcUrl' keys.

            Returns
            -------
            dict
                The transformed dictionary with updated 'customizedJdbcUrl' values.
            """
            for key, sub_dict in merged_data.items():
                if 'customizedJdbcUrl' not in sub_dict:
                    connection_type = sub_dict.get('connection_type', '')
                    host = sub_dict.get('host', '')
                    port = sub_dict.get('port', '')
                    jdbcUseSSL = sub_dict.get('jdbcUseSSL', '')
                    username = sub_dict.get('username', '')
                    password = sub_dict.get('password', '')
                    sub_dict['customizedJdbcUrl'] = (
                        f"jdbc:{connection_type}://{host}:{port};"
                        f"encrypt={jdbcUseSSL};user={username};password={password};"
                    )
            return merged_data

        merged_connections_data = cribl_databaseType(merged_data)
        merged_connections_data = cribl_connectionString(merged_connections_data).items()

        return merged_connections_data
    def load_connections(self, file_names: list | None = None) -> list[BaseModel] | None:
        merged_data = self.merge_examples_connections(file_names)
        connections_obj = [
            ConnectionSchema(
                id=f"{key}-{uuid4()}",
                databaseType=row.get('connection_type'),
                username=row.get('username'),
                password=row.get('password'),
                connectionString=row.get('customizedJdbcUrl'),
                database=row.get('database'),
                disabled=row.get('disabled'),
                host=row.get('host'),
                identity=row.get('identity'),
                jdbcUseSSL=row.get('jdbcUseSSL'),
                localTimezoneConversionEnabled=row.get('localTimezoneConversionEnabled'),
                port=row.get('port'),
                readonly=row.get('readonly'),
                timezone=row.get('timezone')
            )
            for key, row in merged_data
        ]

        self.connection = connections_obj

        return self.connection

    def post_db_connections(
            self,
            base_url: str = "http://localhost:19000",
            cribl_workergroup_name: str = "default",
    ) -> list[dict]:
        return [
            post_new_database_connection(
                base_url=base_url,
                cribl_authtoken=self.token,
                cribl_workergroup_name=cribl_workergroup_name,
                payload=i.model_dump_json(),
            )
            for i in self.connection
        ]
