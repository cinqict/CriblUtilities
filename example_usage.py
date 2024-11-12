# %%
from ingest import Ingestor
# %%
# Now we can use the Ingestor class to load the configuration files
local_ingestor = Ingestor()
# %%
_ = local_ingestor.load_authentication()
_ = local_ingestor.load_input()
_ = local_ingestor.load_connection()
_ = local_ingestor.get_cribl_authtoken()
# %%
# example connection payload
local_ingestor.connection[0].model_dump_json()
#print(local_ingestor.token)
#print('local_ingestor.connection[0].model_dump_json()   ',local_ingestor.connection[0].model_dump_json())
#print('local_ingestor.connection  ',local_ingestor.connection)
# print('local_ingestor.input[0].model_dump_json()   ',local_ingestor.input[0].model_dump_json())
# print('local_ingestor.input  ',local_ingestor.input)
# %%
#responses_connections = local_ingestor.post_connections()
print([i.model_dump_json() for i in local_ingestor.input][0])
responses_inputs = local_ingestor.post_inputs()

# %%
#print(responses_connections)
print(responses_inputs)