# %%
from ingest import Ingestor

# %%
# Now we can use the Ingestor class to load the configuration files
local_ingestor = Ingestor(config_folder="examples")
# %%
_ = local_ingestor.load_identities()
_ = local_ingestor.load_db_connections()
_ = local_ingestor.load_db_inputs()
# this will not run if you do not have a local cribl instance running
# _ = local_ingestor.get_cribl_authtoken()

# %%
# string representation of the ingestor object
# in the background, the __str__ method is called
print(local_ingestor)

# %%
# example db connection payload
print(local_ingestor.db_connections[0].model_dump_json(indent=2))

# %%
# example db input payload
print(local_ingestor.db_inputs[0].model_dump_json(indent=2))

# %%
# example identity payload
print(local_ingestor.identities[0].model_dump_json(indent=2))
