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
    #_ = local_ingestor.load_input()
    _ = local_ingestor.get_cribl_authtoken()
    # print(local_ingestor)
    # %%
    # print(local_ingestor.connection[0].model_dump_json())
    # print(local_ingestor.token)
    # print('local_ingestor.connection[0].model_dump_json()   ',local_ingestor.connection[0].model_dump_json())
    # print('local_ingestor.connection  ',local_ingestor.connection)
    # print('local_ingestor.input[0].model_dump_json()   ',local_ingestor.input[0].model_dump_json())
    # print('local_ingestor.input  ',local_ingestor.input)
    # %%
    connections_data = local_ingestor.merge_examples_connections()
    #print(connections_data)
    _ = local_ingestor.load_connections()
    # print(_)
    response = local_ingestor.post_db_connections()
    print('RESPONSE: ', response)