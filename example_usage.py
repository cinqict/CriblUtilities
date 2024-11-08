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
# %%
responses = local_ingestor.post_connections()
# %%
print(responses)