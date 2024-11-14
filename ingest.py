from pydantic import BaseModel
from schemas import DbConnectionsSchema, DbInputsSchema, IdentitiesSchema
import tomli
import re
from rest_utilities import get_cribl_authentication_token, post_new_database_connection
from uuid import uuid4


def load_config(file: str, schema: type) -> list[BaseModel]:
    """Load a TOML file and validate it against a Pydantic schema.

    Parameters
    ----------
    file : str
        The path to the TOML file.
    schema : type
        The Pydantic schema to validate the TOML file against.

    Returns
    -------
    list[BaseModel]
        A list of Pydantic models.

    """
    with open(file) as f:
        tmp = f.read()
        # .conf files aren't exactly TOML, so we need to format it a bit
        # first before we can load it
        # first replace backslash multilines with single line
        tmp = re.sub(r"\\\n", " ", tmp)
        # then convert string values to quoted strings
        # we use triple quotes as it is possible that the string values
        # contain single or double quotes
        tmp_formatted = re.sub(r"(\s*=\s*)(.*)", r"\1'''\2'''", tmp)
        return [
            schema(**row, id=f"{key}-{uuid4()}") for key, row in tomli.loads(tmp_formatted).items()
        ]


class Ingestor:
    def __init__(
        self,
        config_folder: str = "config",
    ):
        self.config_folder = config_folder
        self.db_connections = None
        self.db_inputs = None
        self.identities = None

    def __str__(self):
        return f"Config folder: {self.config_folder} \nDb Connections: {self.db_connections} \nDb Inputs: {self.db_inputs} \nIdentities: {self.identities}"

    def get_cribl_authtoken(self, base_url: str = "http://localhost:19000") -> str:
        self.token = get_cribl_authentication_token(base_url=base_url)

    def load_db_connections(
        self, file_name: str | None = None
    ) -> list[BaseModel] | None:
        if file_name:
            path = f"{self.config_folder}/{file_name}"
        else:
            path = f"{self.config_folder}/db_connections.conf"
        self.db_connections = load_config(
            file=path,
            schema=DbConnectionsSchema,
        )
        return self.db_connections

    def load_db_inputs(self, file_name: str | None = None) -> list[BaseModel] | None:
        if file_name:
            path = f"{self.config_folder}/{file_name}"
        else:
            path = f"{self.config_folder}/db_inputs.conf"
        self.db_inputs = load_config(
            file=path,
            schema=DbInputsSchema,
        )
        return self.db_inputs

    def load_identities(self, file_name: str | None = None) -> list[BaseModel] | None:
        if file_name:
            path = f"{self.config_folder}/{file_name}"
        else:
            path = f"{self.config_folder}/identities.conf"
        self.identities = load_config(
            file=path,
            schema=IdentitiesSchema,
        )
        return self.identities

    # TODO: this needs to be rewritten
    # due to change in files - we need to merge the three files into
    # 2 post requests
    
    # def post_connections(
    #     self,
    #     base_url: str = "http://localhost:19000",
    #     cribl_workergroup_name: str = "default",
    # ) -> list[dict]:
    #     return [
    #         post_new_database_connection(
    #             base_url=base_url,
    #             cribl_authtoken=self.token,
    #             cribl_workergroup_name=cribl_workergroup_name,
    #             payload=i.model_dump_json(),
    #         )
    #         for i in self.connection
    #     ]
        
