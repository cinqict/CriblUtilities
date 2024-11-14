from pydantic import BaseModel
from schemas import AuthenticationSchema, ConnectionSchema, InputSchema, Metadata, Schedule, Collector, CollectorConf, Run, InputType
import tomli
import re
from rest_utilities import get_cribl_authentication_token, post_new_database_connection, post_new_input
from uuid import uuid4
from typing import List, Tuple, Dict, Any


def load_input_examples(files: List[str]) -> tuple[object, object]:
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

    def load_and_format_db_inputs_toml(file_path: str) -> object:
        with open(file_path) as f:
            tmp = f.read()
            transformed_lines = []
            multiline_query = False
            for line in tmp.split('\n'):
                line = re.sub(r"\s*=\s*", " = ", line)
                if 'query' in line:
                    if '\\' in line:
                        query_content = line.split('query = ')[1].rstrip("\\").strip()
                        # Append the modified 'query' line with triple quotes
                        transformed_lines.append("query = '''")
                        # Append the original content on a new line
                        transformed_lines.append(query_content)
                        multiline_query = True
                    else:
                        # Add other lines as they are
                        transformed_lines.append(line)
                        multiline_query = False

                elif multiline_query == True and '\\' in line:
                    transformed_lines.append(line)
                    multiline_query = True

                elif multiline_query == True and '\\' not in line:
                    transformed_lines.append(line)
                    transformed_lines.append("'''")
                    multiline_query = False
                else:
                    transformed_lines.append(line)

        transformed_text = "\n".join(transformed_lines)
        text = transformed_text.strip()
        # Wrap the text with triple double quotes, starting and ending on a new line
        formatted_text = f"""\n{text}\n"""
        tmp = re.sub(r"\\\n", "\n", formatted_text)
        tmp = re.sub(r"(\s*=\s*)(.*)", r"\1'\2'", tmp)
        tomli_db_inputs = tomli.loads(tmp).items()
        return tomli_db_inputs

    def load_and_format_db_connections(file_path: str) -> object:
        with open(file_path) as f:
            tmp = f.read()
            tmp_formatted = re.sub(r"(\s*=\s*)(.*)", r"\1'\2'", tmp)
            tomli_db_connections = tomli.loads(tmp_formatted).items()
        return tomli_db_connections

    # Load and parse each file
    dict_items1 = load_and_format_db_inputs_toml(files[0])
    dict_items2 = load_and_format_db_connections(files[1])

    return dict_items1, dict_items2


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

    def get_cribl_authtoken(self, base_url: str = "http://localhost:19000") -> str:
        self.token = get_cribl_authentication_token(base_url=base_url)


    def merge_examples_input(self, file_names: list | None = None):
        if file_names and file_names[0]:
            path1 = f"{self.examples_folder}/{file_names[0]}"
        else:
            path1 = f"{self.examples_folder}/db_inputs.conf"
        if file_names and file_names[1]:
            path2 = f"{self.examples_folder}/{file_names[1]}"
        else:
            path2 = f"{self.examples_folder}/db_connections.conf"

        paths = [path1, path2]

        tomli_db_inputs, tomli_db_connections = load_input_examples(files=paths)

        merged_data = {}
        dict_db_inputs = dict(tomli_db_inputs)
        dict_db_connections = dict(tomli_db_connections)

        for key, input_value in dict_db_inputs.items():
            connection_key = input_value.get("connection")
            connection_data = dict_db_connections.get(connection_key, {})
            merged_data[key] = {**input_value, **connection_data}

        # Transform values in "disabled" entry
        def transform_disabled_values(data: dict):
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

        merged_input_data = transform_disabled_values(merged_data).items()

        return merged_input_data

    def load_input(self, file_names: list | None = None) -> list[BaseModel] | None:
        def create_metadata(data):
            return [
                Metadata(name="host", value=data["host"]),
                Metadata(name="index", value=data["index"]),
                Metadata(name="source", value=data.get("source", "")),
                Metadata(name="sourcetype", value=data["sourcetype"])
            ]

        merged_data = self.merge_examples_input(file_names)
        # Parsing tomli_input to create InputSchema instances
        self.input = [
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

        return self.input





    def load_identities(
        self, file_name: str | None = None
    ) -> list[BaseModel] | None:
        if file_name:
            path = f"{self.examples_folder}/{file_name}"
        else:
            path = f"{self.examples_folder}/identities.conf"
        self.identities = load_input_examples()
        return self.identities

    def load_connection(self, file_name: str | None = None) -> list[BaseModel] | None:
        if file_name:
            path = f"{self.examples_folder}/{file_name}"
        else:
            path = f"{self.examples_folder}/db_connections.conf"
        self.connection = load_input_examples()
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
        
