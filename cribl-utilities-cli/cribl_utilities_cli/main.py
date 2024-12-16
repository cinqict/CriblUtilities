import typer
import json
from cribl_utilities_cli import __version__
from cribl_utilities_cli.ingest import Ingestor

app = typer.Typer()


@app.callback()
def callback():
    """
    This is the main command line interface for the cribl-utilities CLI
    """


@app.command()
def check_version():
    """
    Check the version of the cribl-utilities CLI
    """
    typer.echo(f"cribl-utilities CLI version: {__version__}")


@app.command()
def example_env():
    """
    Print an example .env file
    """
    example_dotenv = """
    # save this file as .env in folder you are running the CLI from

    CRIBL_USERNAME=your_cribl_username
    CRIBL_PASSWORD=your_cribl_password
    BASE_URL=your_base_url
    CRIBL_WORKERGROUP_NAME=your_workergroup_name

    # Optional. Add this prefix for the database-connection id.
    DBCONN_PREFIX=

    # Add this as suffix for the database-connection id
    DBCONN_SUFFIX={guid}

    # Optional. Add this prefix for the database collector source id. 
    DBCOLL_PREFIX=

    # Adds this as suffix for the database collector source id	
    DBCOLL_SUFFIX={guid}
    """
    typer.echo(example_dotenv)


@app.command()
def check_env():
    """
    Check the environment variables
    """
    local_ingestor = Ingestor()
    local_ingestor.check_environment_variables()
    typer.echo("Environment variables are set correctly! \n")


@app.command()
def check_cribl_health():
    """
    Check the health of the Cribl instance
    """
    local_ingestor = Ingestor()
    health_response = local_ingestor.check_cribl_health()
    typer.echo("--- Cribl Instance Health Check ---")
    typer.echo(f"Status: {health_response} \n")


@app.command()
def check_connection():
    """
    Check the connection to the Cribl instance
    """
    local_ingestor = Ingestor()
    # to get the token we need to have the env variables set and the Cribl instance running, so even though this
    # function is meant to get the token, if .env is not set correctly or the Cribl instance is not running it will
    # show the corresponding error message
    local_ingestor.check_environment_variables()
    local_ingestor.check_cribl_health()

    local_ingestor.get_cribl_authtoken()
    typer.echo(f"Connection successful! Token: {local_ingestor.token}\n")


@app.command()
def print_inputs_config(folder_name: str, file_names: list[str] | None = None):
    """
    Load the inputs from the chosen folder

    folder_name : str - The name of the folder where the inputs are stored

    file_names : list[str] | None - The names of the files to load (be aware that order matters
    first file should be the inputs.conf file, second file should be the connections.conf file)
    If None, defaults to ['db_inputs.conf', 'db_connections.conf']

    """
    local_ingestor = Ingestor(examples_folder=folder_name)
    # in order to load input files we need to have the env variables
    local_ingestor.check_environment_variables()
    typer.echo("\nEnvironment variables are set correctly!\n")

    inputs = local_ingestor.load_input(file_names=file_names)
    inputs_ids = [single_input.id for single_input in inputs]
    typer.echo("--- Inputs ---")
    typer.echo("Inputs loaded successfully.\nIDs:")
    for input_id in inputs_ids:
        typer.echo(f"- {input_id}")
    typer.echo("\n")

@app.command()
def post_inputs(folder_name: str, file_names: list[str] | None = None):
    """
    Post the inputs to the Cribl instance

    folder_name : str - The name of the folder where the inputs are stored

    file_names : list[str] | None - The names of the files to load (be aware that order matters
    first file should be the db_inputs.conf file, second file should be the db_connections.conf file)
    If None, defaults to ['db_inputs.conf', 'db_connections.conf']

    """
    local_ingestor = Ingestor(examples_folder=folder_name)
    # in order to post input files we need to have the env variables set, the Cribl instance running
    # and an authentication token
    local_ingestor.check_environment_variables()
    typer.echo("\nEnvironment variables are set correctly!\n")

    health_response = local_ingestor.check_cribl_health()
    typer.echo("--- Cribl Instance Health Check ---")
    typer.echo(f"Status: {health_response}")

    local_ingestor.get_cribl_authtoken()
    typer.echo(f"Connection successful! Token: {local_ingestor.token}\n")

    inputs = local_ingestor.load_input(file_names=file_names)
    inputs_ids = [single_input.id for single_input in inputs]
    typer.echo("--- Inputs ---")
    typer.echo("Inputs loaded successfully.\nIDs:")
    for input_id in inputs_ids:
        typer.echo(f"- {input_id}")

    response_inputs = local_ingestor.post_db_inputs()
    response_inputs_ids = [item['id'] for sublist in response_inputs for item in sublist['items']]
    typer.echo("\nResponse from Cribl (Inputs):")
    for input_id in response_inputs_ids:
        typer.echo(f"- {input_id}")
    typer.echo("\n")


@app.command()
def print_connections_config(folder_name: str, file_names: list[str] | None = None):
    """
    Load the connections from the examples folder

    folder_name : str - The name of the folder where the inputs are stored

    file_names : list[str] | None - The names of the files to load (be aware that order matters
    first file should be the inputs.conf file, second file should be the connections.conf file)
    If None, defaults to ['db_inputs.conf', 'db_connections.conf']

    """
    local_ingestor = Ingestor(examples_folder=folder_name)
    # in order to load connection files we need to have the env variables
    local_ingestor.check_environment_variables()
    connections = local_ingestor.load_connections(file_names=file_names)
    connections_ids = [single_connection.id for single_connection in connections]
    typer.echo("\n--- Connections ---")
    typer.echo("Connections loaded successfully.\nIDs:")
    for connection_id in connections_ids:
        typer.echo(f"- {connection_id}")
    typer.echo("\n")

@app.command()
def post_connections(folder_name: str, file_names: list[str] | None = None):
    """
    Post the connections to the Cribl instance

    folder_name : str - The name of the folder where the inputs are stored

    file_names : list[str] | None - The names of the files to load (be aware that order matters
    first file should be the inputs.conf file, second file should be the connections.conf file)
    If None, defaults to ['db_inputs.conf', 'db_connections.conf']

    """
    local_ingestor = Ingestor(examples_folder=folder_name)
    # in order to post connection files we need to have the env variables set, the Cribl instance running
    # and an authentication token
    local_ingestor.check_environment_variables()
    typer.echo("\nEnvironment variables are set correctly!\n")

    health_response = local_ingestor.check_cribl_health()
    typer.echo("--- Cribl Instance Health Check ---")
    typer.echo(f"Status: {health_response}")

    local_ingestor.get_cribl_authtoken()
    typer.echo(f"Connection successful! Token: {local_ingestor.token}\n")

    connections = local_ingestor.load_connections(file_names=file_names)
    connections_ids = [single_connection.id for single_connection in connections]
    typer.echo("\n--- Connections ---")
    typer.echo("Connections loaded successfully.\nIDs:")
    for connection_id in connections_ids:
        typer.echo(f"- {connection_id}")

    response_connections = local_ingestor.post_db_connections()
    response_connections_ids = [item['id'] for sublist in response_connections for item in sublist['items']]
    typer.echo("\nResponse from Cribl (Connections):")
    for connection_id in response_connections_ids:
        typer.echo(f"- {connection_id}")
    typer.echo("\n")


@app.command()
def run_all(
        folder_name: str,
        file_names: list[str] | None = None,
        save_trace_to_file: bool = False,
):
    """
    Run all the commands in order (print_inputs_config, post_inputs, print_connections_config, post_connections)

    folder_name : str - The name of the folder where the inputs are stored

    file_names : list[str] | None - The names of the files to load (be aware that order matters
    first file should be the inputs.conf file, second file should be the connections.conf file)
    If None, defaults to ['db_inputs.conf', 'db_connections.conf']

    save_trace_to_file : bool - If True, saves the trace to a file

    """
    local_ingestor = Ingestor(examples_folder=folder_name)

    # Step 1: Check environment variables
    local_ingestor.check_environment_variables()
    typer.echo("\nEnvironment variables are set correctly!\n")

    # Step 2: Check Cribl health
    health_response = local_ingestor.check_cribl_health()
    typer.echo("--- Cribl Instance Health Check ---")
    typer.echo(f"Status: {health_response}")

    # Step 3: Get Cribl Auth Token
    local_ingestor.get_cribl_authtoken()
    typer.echo(f"Connection successful! Token: {local_ingestor.token}\n")

    # Step 4: Load and post inputs
    inputs = local_ingestor.load_input(file_names=file_names)
    inputs_ids = [single_input.id for single_input in inputs]
    typer.echo("--- Inputs ---")
    typer.echo("Inputs loaded successfully.\nIDs:")
    for input_id in inputs_ids:
        typer.echo(f"- {input_id}")

    response_inputs = local_ingestor.post_db_inputs()
    response_inputs_ids = [item['id'] for sublist in response_inputs for item in sublist['items']]
    typer.echo("\nResponse from Cribl (Inputs):")
    for input_id in response_inputs_ids:
        typer.echo(f"- {input_id}")

    # Step 5: Load and post connections
    connections = local_ingestor.load_connections(file_names=file_names)
    connections_ids = [single_connection.id for single_connection in connections]
    typer.echo("\n--- Connections ---")
    typer.echo("Connections loaded successfully.\nIDs:")
    for connection_id in connections_ids:
        typer.echo(f"- {connection_id}")

    response_connections = local_ingestor.post_db_connections()
    response_connections_ids = [item['id'] for sublist in response_connections for item in sublist['items']]
    typer.echo("\nResponse from Cribl (Connections):")
    for connection_id in response_connections_ids:
        typer.echo(f"- {connection_id}")

    # Step 6: Save trace to file (if enabled)
    if save_trace_to_file:
        with open("./trace.txt", "w") as f:
            f.write("--- Inputs ---\n")
            f.write(f"Inputs loaded: {[single_input.model_dump() for single_input in inputs]}\n")
            f.write(f"Response from Cribl (Inputs): {response_inputs}\n\n")

            f.write("--- Connections ---\n")
            f.write(f"Connections loaded: {[single_connection.model_dump() for single_connection in connections]}\n")
            f.write(f"Response from Cribl (Connections): {response_connections}\n")

    typer.echo("\nAll steps completed successfully! \n")
