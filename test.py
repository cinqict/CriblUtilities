# %%
from ingest import Ingestor
# %%
# Now we can use the Ingestor class to load the examples files
local_ingestor = Ingestor()
# %%
_ = local_ingestor.get_cribl_authtoken()
# print(local_ingestor.merge_examples_input())
# db_inputs = local_ingestor.load_input()
# print(db_inputs)
#print(db_inputs[0].collector.conf.query)
#response_db_inputs = local_ingestor.post_db_inputs()
#print(response_db_inputs)
#print(local_ingestor.input[0].model_dump_json())


connections_data = local_ingestor.merge_examples_connections()
#print(connections_data)
_ = local_ingestor.load_connections()
response = local_ingestor.post_db_connections()
print(response)

