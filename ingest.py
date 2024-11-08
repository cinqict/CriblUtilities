from pydantic import BaseModel
from schemas import AuthenticationSchema, ConnectionSchema, InputSchema
import tomli
import re


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
        tmp_formatted = re.sub(r'(\s*=\s*)(.*)', r'\1"\2"', tmp)
        return [
            schema(**i) for i in tomli.loads(tmp_formatted).values()
        ]
    

class Ingestor:
    def __init__(self, authentication: AuthenticationSchema, connection: ConnectionSchema, input: InputSchema):
        self.authentication = authentication
        self.connection = connection
        self.input = input

    def __str__(self):
        return f'Authentication: {self.authentication}\nConnection: {self.connection}\nInput: {self.input}'