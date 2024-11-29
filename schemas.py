#
#           .:-=====-:.         ---   :--:            .--:           .--====-:.                
#     :=*####***####*+:     :###.  =###*.          -##*        -+#####**####*=:             
#   .*##*=:.     .:=*#=     :###.  =#####-         -##*      =###+-.      :=*##*:           
#  -###-                    :###.  =##++##+        -##*    .*##+.            -###=          
# :###:                     :###.  =##+ +##*.      -##*    *##=               .*##=         
# *##=                      :###.  =##+  -###-     -##*   =##*                 -###         
# ###-                      :###.  =##+   .*##+    -##*   +##+                 .###.        
# ###=                      :###.  =##+     =##*.  -##*   =##*           :     :###.        
# =##*.                     :###.  =##+      :*##- -##*   .###-         ---:.  *##+         
#  +##*.                    :###.  =##+       .*##+-##*    -###-         .----=##*          
#   =###+:         .-**.    :###.  =##+         =##*##*     :*##*-         -=--==       ... 
#    .=####+==-==+*###+:    :###.  =##+          :*###*       -*###*+=-==+###+----.    ----:
#       :=+*####**+=:       .***   =**=            +**+         .-=+*####*+=:  .:-.    .---.
#                                                                                           
#                                                                                          
#   Copyright 2024 CINQ ICT b.v.
#
#   Licensed under the Apache License, Version 2.0 (the "License");
#   you may not use this file except in compliance with the License.
#   You may obtain a copy of the License at
#
#       http://www.apache.org/licenses/LICENSE-2.0
#
#   Unless required by applicable law or agreed to in writing, software
#   distributed under the License is distributed on an "AS IS" BASIS,
#   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#   See the License for the specific language governing permissions and
#   limitations under the License.

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
    class ConfigDict:
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
    connectionString: Optional[str] = Field(default=None, json_schema_extra={"exclude_none": True})
    configObj: Optional[dict] = Field(default=None, json_schema_extra={"exclude_none": True})
    localTimezoneConversionEnabled: Optional[bool]
    port: int
    readonly: Optional[bool]
    timezone: Optional[str]
    authType: str