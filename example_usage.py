# %%
from ingest import Ingestor
import sys
# %%

if sys.version_info < (3, 10):
    raise RuntimeError("This project requires Python 3.10 or higher.")
else:
    # Now we can use the Ingestor class to load the examples files
    local_ingestor = Ingestor()
    # %%
    _ = local_ingestor.get_cribl_authtoken()
    # %%
    inputs = local_ingestor.load_input()
    response_inputs = local_ingestor.post_db_inputs()
    print('RESPONSE INPUTS API: ', response_inputs)
    # %%
    connections = local_ingestor.load_connections()
    response_connections = local_ingestor.post_db_connections()
    print('RESPONSE CONNECTIONS API: ', response_connections)