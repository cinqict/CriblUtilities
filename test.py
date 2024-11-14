# %%
from ingest import Ingestor
# %%
# Now we can use the Ingestor class to load the examples files
local_ingestor = Ingestor()
# %%
_ = local_ingestor.get_cribl_authtoken()
data_merged = local_ingestor.transform_input()
print(data_merged)
db_inputs = local_ingestor.load_input()
print(db_inputs)
response_db_inputs = local_ingestor.post_db_inputs()
print(response_db_inputs)
