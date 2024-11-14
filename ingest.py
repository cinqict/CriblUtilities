from pydantic import BaseModel
from schemas import AuthenticationSchema, ConnectionSchema, InputSchema, Metadata, Schedule, Collector, CollectorConf, Run, InputType
import tomli
import re
from rest_utilities import get_cribl_authentication_token, post_new_database_connection, post_new_input
from uuid import uuid4


def load_examples(files: list) -> list[BaseModel]:
    """Load TOML files and validate it against a Pydantic schema.

    Parameters
    ----------
    file : list
        The path to the TOML files.

    Returns
    -------
    dict_items1, dict_items2: dictionary items
        Two dictionaries with the data from the TOML files

    """
    # with open(files) as f:
    #     tmp = f.read()
    #     # .conf files aren't exactly TOML, so we need to format it a bit
    #     # first before we can load it
    #     tmp_formatted = re.sub(r"(\s*=\s*)(.*)", r"\1'\2'", tmp)
    #     return [
    #         schema(**row, id=f"{key}-{uuid4()}") for key, row in tomli.loads(tmp_formatted).items()
    #     ]


    with open(files[0]) as f:
        tmp = f.read()
        # .conf files aren't exactly TOML, so we need to format it a bit
        # first before we can load it
        tmp_formatted = re.sub(r"(\s*=\s*)(.*)", r"\1'\2'", tmp)
        dict_items1 = tomli.loads(tmp_formatted).items()

    with open(files[1]) as f:
        tmp = f.read()
        tmp_formatted = re.sub(r"(\s*=\s*)(.*)", r"\1'\2'", tmp)
        dict_items2 = tomli.loads(tmp_formatted).items()

    return dict_items1, dict_items2

class Ingestor:
    def __init__(
        self,
        examples_folder: str = "examples",
    ):
        self.transformed_input_data = None
        self.examples_folder = examples_folder
        self.identities = None
        self.connection = None
        self.input = None

    def __str__(self):
        return f"Authentication: {self.identities}\nConnection: {self.connection}\nInput: {self.input}"

    def get_cribl_authtoken(self, base_url: str = "http://localhost:19000") -> str:
        self.token = get_cribl_authentication_token(base_url=base_url)

    def transform_input(self, file_names: list | None = None):
        if file_names and file_names[0]:
            path1 = f"{self.examples_folder}/{file_names[0]}"
        else:
            path1 = f"{self.examples_folder}/db_inputs.conf"
        if file_names and file_names[1]:
            path2 = f"{self.examples_folder}/{file_names[1]}"
        else:
            path2 = f"{self.examples_folder}/db_connections.conf"

        paths = [path1, path2]

        tomli_db_inputs, tomli_db_connections = load_examples(files = paths)

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

        self.transformed_input_data = transform_disabled_values(merged_data).items()

        return self.transformed_input_data


    def load_input(self) -> list[BaseModel] | None:
        def create_metadata(data):
            return [
                Metadata(name="host", value=data["host"]),
                Metadata(name="index", value=data["index"]),
                Metadata(name="source", value=data["source"]),
                Metadata(name="sourcetype", value=data["sourcetype"])
            ]

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
            for key, row in self.transformed_input_data
        ]

        return self.input

    def load_identities(
        self, file_name: str | None = None
    ) -> list[BaseModel] | None:
        if file_name:
            path = f"{self.examples_folder}/{file_name}"
        else:
            path = f"{self.examples_folder}/identities.conf"
        self.identities = load_examples(
            file=path,
            schema=AuthenticationSchema,
        )
        return self.identities

    def load_connection(self, file_name: str | None = None) -> list[BaseModel] | None:
        if file_name:
            path = f"{self.examples_folder}/{file_name}"
        else:
            path = f"{self.examples_folder}/db_connections.conf"
        self.connection = load_examples(
            file=path,
            schema=ConnectionSchema,
        )
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
        
