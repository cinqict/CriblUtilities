from pydantic import BaseModel, ConfigDict, field_validator


class BaseSchema(BaseModel):
    model_config = ConfigDict(
        # alias_generator=to_camel,
        populate_by_name=True,
    )

class DbConnectionsSchema(BaseSchema):
    id: str
    connection_type: str
    database: str
    disabled: int
    host: str
    identity: str
    jdbcUseSSL: bool
    port: int
    readonly: bool
    timezone: str | None = None
    customizedJdbcUrl: str | None = None
    connection_properties: str | None = None
    localTimezoneConversionEnabled: bool = None


class DbInputsSchema(BaseSchema):
    id: str
    connection: str
    description: str | None = None
    disabled: int
    host: str
    index: str
    index_time_mode: str | None = None
    interval: str
    mode: str
    query: str
    source: str | None = None
    sourcetype: str
    input_timestamp_column_number: int | None = None
    query_timeout: int | None = None
    tail_rising_column_name: str | None = None
    ui_query_catalog: str | None = None
    ui_query_mode: str | None = None
    ui_query_schema: str | None = None
    ui_query_table: str | None = None
    fetch_size: int | None = None
    batch_upload_size: int | None = None
    max_single_checkpoint_file_size: int | None = None
    max_rows: int | None = None

    
class IdentitiesSchema(BaseSchema):
    id: str
    disabled: int
    password: str
    use_win_auth: int
    username: str
    domain_name: str | None = None
    