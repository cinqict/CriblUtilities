from pydantic import BaseModel, ConfigDict, field_validator
from typing import List, Dict, Optional

class BaseSchema(BaseModel):
    model_config = ConfigDict(
        # alias_generator=to_camel,
        populate_by_name=True,
    )


class AuthenticationSchema(BaseSchema):
    disabled: int
    password: str
    use_win_auth: int
    username: str

class ScheduleSchema(BaseModel):
    cronSchedule: str = "0 6 * * *"
    run: Dict[str, str] = {"mode": "batch"}
    enabled: bool = True

class CollectorConfSchema(BaseModel):
    connectionId: str = "default_connection"
    query: str = "\"SELECT * FROM OWNER.CONFIG_SPLUNK\"" #placeholder

class CollectorSchema(BaseModel):
    conf: CollectorConfSchema = CollectorConfSchema()
    type: str = "database"

class MetadataSchema(BaseModel):
    name: str
    value: str

class InputSchema(BaseModel):
    # Fields with default values
    type: str = "collection"  # Default to "collection"
    schedule: ScheduleSchema = ScheduleSchema()  # Default ScheduleSchema instance
    collector: CollectorSchema = CollectorSchema()  # Default CollectorSchema instance
    input: Dict[str, List[MetadataSchema]] = {
        "type": "collection",
        "metadata": [
            MetadataSchema(name="index", value="default_index"),
            MetadataSchema(name="sourcetype", value="default_sourcetype"),
            MetadataSchema(name="source", value="default_source")
        ]
    }  # Default metadata entries

    # Required fields without defaults
    connection: str
    disabled: int
    host: str
    index: str
    index_time_mode: str
    interval: str
    max_rows: int
    mode: str
    query: str
    source: str
    sourcetype: str
    id: str


class ConnectionSchema(BaseSchema):
    id: str | None = None
    connection_type: str
    customizedJdbcUrl: str | None = None
    database: str
    disabled: int
    host: str
    identity: str
    jdbcUseSSL: bool
    localTimezoneConversionEnabled: bool
    port: int
    readonly: bool
    timezone: str | None = None
