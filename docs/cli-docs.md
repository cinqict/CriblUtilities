# `cribl-utilities`

This is the main command line interface for the cribl-utilities CLI

**Usage**:

```console
$ cribl-utilities [OPTIONS] COMMAND [ARGS]...
```

**Options**:

* `--install-completion`: Install completion for the current shell.
* `--show-completion`: Show completion for the current shell, to copy it or customize the installation.
* `--help`: Show this message and exit.

**Commands**:

* `example-env`: Print an example of an environment...
* `setup`: Prompt the user for environment variables...
* `print-inputs-config`: Load the inputs from the chosen folder and...
* `post-inputs`: Post the inputs to the Cribl instance
* `print-connections-config`: Load the connections from the examples...
* `post-connections`: Post the connections to the Cribl instance
* `migrate-database`: Check the environment variables, Cribl...
* `check`: Perform various checks related to Cribl...

## `cribl-utilities example-env`

Print an example of an environment variables file

**Usage**:

```console
$ cribl-utilities example-env [OPTIONS]
```

**Options**:

* `--help`: Show this message and exit.

## `cribl-utilities setup`

Prompt the user for environment variables and save them to a file

**Usage**:

```console
$ cribl-utilities setup [OPTIONS]
```

**Options**:

* `--help`: Show this message and exit.

## `cribl-utilities print-inputs-config`

Load the inputs from the chosen folder and print them

folder_name : str - The name of the folder where the inputs are stored

file_names : list | None - The names of the files to load (be aware that order matters
first file should be the inputs.conf file, second file should be the connections.conf file)
If None, defaults to [&#x27;db_inputs.conf&#x27;, &#x27;db_connections.conf&#x27;]

**Usage**:

```console
$ cribl-utilities print-inputs-config [OPTIONS] FOLDER_NAME
```

**Arguments**:

* `FOLDER_NAME`: [required]

**Options**:

* `--file-names TEXT`
* `--help`: Show this message and exit.

## `cribl-utilities post-inputs`

Post the inputs to the Cribl instance

folder_name : str - The name of the folder where the inputs are stored

file_names : list | None - The names of the files to load (be aware that order matters
first file should be the db_inputs.conf file, second file should be the db_connections.conf file)
If None, defaults to [&#x27;db_inputs.conf&#x27;, &#x27;db_connections.conf&#x27;]

**Usage**:

```console
$ cribl-utilities post-inputs [OPTIONS] FOLDER_NAME
```

**Arguments**:

* `FOLDER_NAME`: [required]

**Options**:

* `--file-names TEXT`
* `--help`: Show this message and exit.

## `cribl-utilities print-connections-config`

Load the connections from the examples folder and print them

folder_name : str - The name of the folder where the inputs are stored

file_names : list | None - The names of the files to load (be aware that order matters
first file should be the inputs.conf file, second file should be the connections.conf file)
If None, defaults to [&#x27;db_inputs.conf&#x27;, &#x27;db_connections.conf&#x27;]

**Usage**:

```console
$ cribl-utilities print-connections-config [OPTIONS] FOLDER_NAME
```

**Arguments**:

* `FOLDER_NAME`: [required]

**Options**:

* `--file-names TEXT`
* `--help`: Show this message and exit.

## `cribl-utilities post-connections`

Post the connections to the Cribl instance

folder_name : str - The name of the folder where the inputs are stored

file_names : list | None - The names of the files to load (be aware that order matters
first file should be the inputs.conf file, second file should be the connections.conf file)
If None, defaults to [&#x27;db_inputs.conf&#x27;, &#x27;db_connections.conf&#x27;]

**Usage**:

```console
$ cribl-utilities post-connections [OPTIONS] FOLDER_NAME
```

**Arguments**:

* `FOLDER_NAME`: [required]

**Options**:

* `--file-names TEXT`
* `--help`: Show this message and exit.

## `cribl-utilities migrate-database`

Check the environment variables, Cribl health, get the Cribl auth token, load and post inputs and connections,
and save the trace to a file

folder_name : str - The name of the folder where the inputs are stored

file_names : list | None - The names of the files to load (be aware that order matters
first file should be the inputs.conf file, second file should be the connections.conf file)
If None, defaults to [&#x27;db_inputs.conf&#x27;, &#x27;db_connections.conf&#x27;]

save_trace_to_file : bool - If True, saves the trace to a file

**Usage**:

```console
$ cribl-utilities migrate-database [OPTIONS] FOLDER_NAME
```

**Arguments**:

* `FOLDER_NAME`: [required]

**Options**:

* `--file-names TEXT`
* `--save-trace-to-file / --no-save-trace-to-file`: [default: no-save-trace-to-file]
* `--help`: Show this message and exit.

## `cribl-utilities check`

Perform various checks related to Cribl utilities. Type `cribl-utilities check --help` to see subcommands

**Usage**:

```console
$ cribl-utilities check [OPTIONS] COMMAND [ARGS]...
```

**Options**:

* `--help`: Show this message and exit.

**Commands**:

* `version`: Check the version of the cribl-utilities CLI
* `env`: Check the environment variables
* `cribl-health`: Check the health of the Cribl instance
* `connection`: Check the connection to the Cribl instance
* `files`: Checks if expected files are adhering to...
* `naming`: Check the naming convention of the field...

### `cribl-utilities check version`

Check the version of the cribl-utilities CLI

**Usage**:

```console
$ cribl-utilities check version [OPTIONS]
```

**Options**:

* `--help`: Show this message and exit.

### `cribl-utilities check env`

Check the environment variables

**Usage**:

```console
$ cribl-utilities check env [OPTIONS]
```

**Options**:

* `--help`: Show this message and exit.

### `cribl-utilities check cribl-health`

Check the health of the Cribl instance

**Usage**:

```console
$ cribl-utilities check cribl-health [OPTIONS]
```

**Options**:

* `--help`: Show this message and exit.

### `cribl-utilities check connection`

Check the connection to the Cribl instance

**Usage**:

```console
$ cribl-utilities check connection [OPTIONS]
```

**Options**:

* `--help`: Show this message and exit.

### `cribl-utilities check files`

Checks if expected files are adhering to YAML linting. Basic syntax validation

conf : str - The cribl-config folder where the YAML files are stored

**Usage**:

```console
$ cribl-utilities check files [OPTIONS]
```

**Options**:

* `--conf TEXT`: cribl-config folder where the YAML files are stored  [required]
* `--help`: Show this message and exit.

### `cribl-utilities check naming`

Check the naming convention of the field in the YAML files

Parameters
----------
conf : str - The cribl-config folder where the YAML files are stored
field : str - Field to check naming convention for in the YAML files
regex : str - Regex to check the field against
exceptions : list - The fields to exclude from the check
debug : bool - Flag to enable debug option

Returns
-------

**Usage**:

```console
$ cribl-utilities check naming [OPTIONS]
```

**Options**:

* `--conf TEXT`: cribl-config folder where the YAML files are stored  [required]
* `--field TEXT`: Field to check naming convention for in the YAML files.
Options: workergroup, sources, destinations, dataroutes, pipelines, packs.  [required]
* `--regex TEXT`: Regex to check the field against
* `--exceptions TEXT`: List of exceptions to the naming convention
* `--debug / --no-debug`: Debug option   [default: no-debug]
* `--help`: Show this message and exit.
