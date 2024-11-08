from pydantic import BaseModel, ConfigDict


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


class InputSchema(BaseSchema):
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


class ConnectionSchema(BaseSchema):
    connection_type: str
    customizedJdbcUrl: str
    database: str
    disabled: int
    host: str
    identity: str
    jdbcUseSSL: bool
    localTimezoneConversionEnabled: bool
    port: int
    readonly: bool
    timezone: str