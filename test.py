# %%
from ingest import Ingestor
# %%
# Now we can use the Ingestor class to load the configuration files
local_ingestor = Ingestor()
# %%
_ = local_ingestor.get_cribl_authtoken()
data_merged = local_ingestor.transform_input()
print(data_merged)
inputs = local_ingestor.load_input()
print(inputs)
response_inputs = local_ingestor.post_inputs()
print(response_inputs)
