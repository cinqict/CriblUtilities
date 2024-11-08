from pydantic import BaseModel
from schemas import AuthenticationSchema, ConnectionSchema, InputSchema
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
        tmp_formatted = re.sub(r"(\s*=\s*)(.*)", r"\1'\2'", tmp)
        return [
            schema(**row, id=f"{key}-{uuid4()}") for key, row in tomli.loads(tmp_formatted).items()
        ]


class Ingestor:
    def __init__(
        self,
        config_folder: str = "config",
    ):
        self.config_folder = config_folder
        self.authentication = None
        self.connection = None
        self.input = None

    def __str__(self):
        return f"Authentication: {self.authentication}\nConnection: {self.connection}\nInput: {self.input}"

    def get_cribl_authtoken(self, base_url: str = "http://localhost:19000") -> str:
        self.token = get_cribl_authentication_token(base_url=base_url)

    def load_authentication(
        self, file_name: str | None = None
    ) -> list[BaseModel] | None:
        if file_name:
            path = f"{self.config_folder}/{file_name}"
        else:
            path = f"{self.config_folder}/authentication.conf"
        self.authentication = load_config(
            file=path,
            schema=AuthenticationSchema,
        )
        return self.authentication

    def load_connection(self, file_name: str | None = None) -> list[BaseModel] | None:
        if file_name:
            path = f"{self.config_folder}/{file_name}"
        else:
            path = f"{self.config_folder}/connections.conf"
        self.connection = load_config(
            file=path,
            schema=ConnectionSchema,
        )
        return self.connection

    def load_input(self, file_name: str | None = None) -> list[BaseModel] | None:
        if file_name:
            path = f"{self.config_folder}/{file_name}"
        else:
            path = f"{self.config_folder}/inputs.conf"
        self.input = load_config(
            file=path,
            schema=InputSchema,
        )
        return self.input

    def post_connections(
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
