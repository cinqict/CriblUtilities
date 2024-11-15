# %%
from ingest import Ingestor
# %%
# Now we can use the Ingestor class to load the examples files
local_ingestor = Ingestor()
# %%
_ = local_ingestor.get_cribl_authtoken()

db_inputs = local_ingestor.load_input()
#print(db_inputs)
#print(db_inputs[0].collector.conf.query)
response_db_inputs = local_ingestor.post_db_inputs()
print(response_db_inputs)
#print(local_ingestor.input[0].model_dump_json())
