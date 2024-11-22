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
#   Splunk Cribl Utilities helps managing the Cribl environment
#   Copyright (C) 2024  CINQ ICT
#
#   This program is free software: you can redistribute it and/or modify
#   it under the terms of the GNU Affero General Public License as
#   published by the Free Software Foundation, either version 3 of the
#   License, or (at your option) any later version.
#
#   This program is distributed in the hope that it will be useful,
#   but WITHOUT ANY WARRANTY; without even the implied warranty of
#   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#   GNU Affero General Public License for more details.
#
#   You should have received a copy of the GNU Affero General Public License
#   along with this program.  If not, see <https://www.gnu.org/licenses/>.

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