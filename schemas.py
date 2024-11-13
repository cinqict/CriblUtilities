from pydantic import BaseModel, ConfigDict, Field
from typing import List, Optional

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

class Metadata(BaseModel):
    name: str
    value: str

class Run(BaseModel):
    mode: str

class Schedule(BaseModel):
    cronSchedule: str = Field(alias='interval')
    run: Run
    enabled: bool = Field(alias='disabled')

class CollectorConf(BaseModel):
    connectionId: str = Field(alias='connection')
    query: str

class Collector(BaseModel):
    conf: CollectorConf
    type: str = "database"

class InputType(BaseModel):
    type: str = "collection"
    metadata: List[Metadata]

class InputSchema(BaseModel):
    type: Optional[str] = "collection"
    schedule: Schedule
    collector: Collector
    input: InputType
    id: Optional[str]


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
