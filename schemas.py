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


class ConnectionSchema(BaseModel):
    class Config:
        extra = 'ignore'

    id: Optional[str]
    databaseType: Optional[str]
    username: str
    password: str
    database: str
    disabled: int
    host: str
    identity: str
    jdbcUseSSL: bool
    connectionString: Optional[str] = Field(default=None, exclude_none=True)
    configObj: Optional[dict] = Field(default=None, exclude_none=True)
    localTimezoneConversionEnabled: Optional[bool]
    port: int
    readonly: Optional[bool]
    timezone: Optional[str]
    authType: str