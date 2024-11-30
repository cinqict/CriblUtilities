import typer
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
def check_cribl_health():
    """
    Check the health of the Cribl instance
    """
    local_ingestor = Ingestor()
    # bit of a weird name considering it's checking the health of the Cribl instance
    health_response = local_ingestor.check_docker_running()
    typer.echo(f"Response from Cribl instance: {health_response}")


@app.command()
def check_connection():
    """
    Check the connection to the Cribl instance
    """
    local_ingestor = Ingestor()
    local_ingestor.get_cribl_authtoken()
    typer.echo(
        f"Connection to Cribl instance successful! token: {local_ingestor.token}"
    )


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
    inputs = local_ingestor.load_input(file_names=file_names)
    typer.echo(
        f"Inputs loaded: {[single_input.model_dump() for single_input in inputs]}"
    )


@app.command()
def post_inputs(folder_name: str, file_names: list[str] | None = None):
    """
    Post the inputs to the Cribl instance

    folder_name : str - The name of the folder where the inputs are stored

    file_names : list[str] | None - The names of the files to load (be aware that order matters
    first file should be the inputs.conf file, second file should be the connections.conf file)
    If None, defaults to ['db_inputs.conf', 'db_connections.conf']

    """
    local_ingestor = Ingestor(examples_folder=folder_name)
    local_ingestor.get_cribl_authtoken()
    inputs = local_ingestor.load_input(file_names=file_names)
    typer.echo(
        f"Inputs loaded: {[single_input.model_dump() for single_input in inputs]}"
    )
    response_inputs = local_ingestor.post_db_inputs()
    typer.echo(f"Response from Cribl instance: {response_inputs}")


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
    connections = local_ingestor.load_connections(file_names=file_names)
    typer.echo(
        f"Connections loaded: {[single_connection.model_dump() for single_connection in connections]}"
    )


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
    local_ingestor.get_cribl_authtoken()
    connections = local_ingestor.load_connections(file_names=file_names)
    typer.echo(
        f"Connections loaded: {[single_connection.model_dump() for single_connection in connections]}"
    )
    response_connections = local_ingestor.post_db_connections()
    typer.echo(f"Response from Cribl instance: {response_connections}")


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
    local_ingestor.get_cribl_authtoken()
    typer.echo(
        f"Connection to Cribl instance successful! token: {local_ingestor.token}"
    )
    inputs = local_ingestor.load_input(file_names=file_names)
    typer.echo(
        f"Inputs loaded: {[single_input.model_dump() for single_input in inputs]}"
    )
    response_inputs = local_ingestor.post_db_inputs()
    typer.echo(f"Response from Cribl instance: {response_inputs}")
    connections = local_ingestor.load_connections(file_names=file_names)
    typer.echo(
        f"Connections loaded: {[single_connection.model_dump() for single_connection in connections]}"
    )
    response_connections = local_ingestor.post_db_connections()
    typer.echo(f"Response from Cribl instance: {response_connections}")

    if save_trace_to_file:
        with open("./trace.txt", "w") as f:
            f.write(
                f"Inputs loaded: {[single_input.model_dump() for single_input in inputs]}\n"
            )
            f.write(f"Response from Cribl instance: {response_inputs}\n")
            f.write(
                f"Connections loaded: {[single_connection.model_dump() for single_connection in connections]}\n"
            )
            f.write(f"Response from Cribl instance: {response_connections}\n")
