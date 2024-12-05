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
# 

# -----------------------------------------------------------------------------------------------------------
# This file is intended to be used as an example of how to use the Ingestor class without the CLI.
# It is heavily suggested to use the CLI directly, but if you want to use the Ingestor class directly, 
# you can do it like this.
# -----------------------------------------------------------------------------------------------------------

from cribl_utilities_cli.ingest import Ingestor
import sys

if sys.version_info < (3, 13):
    raise RuntimeError("This project requires Python 3.13 or higher.")
else:
    # Now we can use the Ingestor class to load the examples files
    local_ingestor = Ingestor()
    
    local_ingestor.get_cribl_authtoken()
    
    inputs = local_ingestor.load_input()
    response_inputs = local_ingestor.post_db_inputs()
    print('RESPONSE INPUTS API: ', response_inputs)

    connections = local_ingestor.load_connections()
    response_connections = local_ingestor.post_db_connections()
    print('RESPONSE CONNECTIONS API: ', response_connections)
