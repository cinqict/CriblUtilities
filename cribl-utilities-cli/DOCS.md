# `cribl-utilities-cli`

This is the main command line interface for the cribl-utilities CLI

**Usage**:

```console
$ cribl-utilities-cli [OPTIONS] COMMAND [ARGS]...
```

**Options**:

* `--install-completion`: Install completion for the current shell.
* `--show-completion`: Show completion for the current shell, to copy it or customize the installation.
* `--help`: Show this message and exit.

**Commands**:

* `check-version`: Check the version of the cribl-utilities CLI
* `example-env`: Print an example .env file
* `check-cribl-health`: Check the health of the Cribl instance
* `check-connection`: Check the connection to the Cribl instance
* `print-inputs-config`: Load the inputs from the chosen folder
* `post-inputs`: Post the inputs to the Cribl instance
* `print-connections-config`: Load the connections from the examples folder
* `post-connections`: Post the connections to the Cribl instance
* `run-all`: Run all the commands in order...

## `cribl-utilities-cli check-version`

Check the version of the cribl-utilities CLI

**Usage**:

```console
$ cribl-utilities-cli check-version [OPTIONS]
```

**Options**:

* `--help`: Show this message and exit.

## `cribl-utilities-cli example-env`

Print an example .env file

**Usage**:

```console
$ cribl-utilities-cli example-env [OPTIONS]
```

**Options**:

* `--help`: Show this message and exit.

## `cribl-utilities-cli check-cribl-health`

Check the health of the Cribl instance

**Usage**:

```console
$ cribl-utilities-cli check-cribl-health [OPTIONS]
```

**Options**:

* `--help`: Show this message and exit.

## `cribl-utilities-cli check-connection`

Check the connection to the Cribl instance

**Usage**:

```console
$ cribl-utilities-cli check-connection [OPTIONS]
```

**Options**:

* `--help`: Show this message and exit.

## `cribl-utilities-cli print-inputs-config`

Load the inputs from the chosen folder

folder_name : str - The name of the folder where the inputs are stored

file_names : list | None - The names of the files to load (be aware that order matters
first file should be the inputs.conf file, second file should be the connections.conf file)
If None, defaults to [&#x27;db_inputs.conf&#x27;, &#x27;db_connections.conf&#x27;]

**Usage**:

```console
$ cribl-utilities-cli print-inputs-config [OPTIONS] FOLDER_NAME
```

**Arguments**:

* `FOLDER_NAME`: [required]

**Options**:

* `--file-names TEXT`
* `--help`: Show this message and exit.

## `cribl-utilities-cli post-inputs`

Post the inputs to the Cribl instance

folder_name : str - The name of the folder where the inputs are stored

file_names : list | None - The names of the files to load (be aware that order matters
first file should be the inputs.conf file, second file should be the connections.conf file)
If None, defaults to [&#x27;db_inputs.conf&#x27;, &#x27;db_connections.conf&#x27;]

**Usage**:

```console
$ cribl-utilities-cli post-inputs [OPTIONS] FOLDER_NAME
```

**Arguments**:

* `FOLDER_NAME`: [required]

**Options**:

* `--file-names TEXT`
* `--help`: Show this message and exit.

## `cribl-utilities-cli print-connections-config`

Load the connections from the examples folder

folder_name : str - The name of the folder where the inputs are stored

file_names : list | None - The names of the files to load (be aware that order matters
first file should be the inputs.conf file, second file should be the connections.conf file)
If None, defaults to [&#x27;db_inputs.conf&#x27;, &#x27;db_connections.conf&#x27;]

**Usage**:

```console
$ cribl-utilities-cli print-connections-config [OPTIONS] FOLDER_NAME
```

**Arguments**:

* `FOLDER_NAME`: [required]

**Options**:

* `--file-names TEXT`
* `--help`: Show this message and exit.

## `cribl-utilities-cli post-connections`

Post the connections to the Cribl instance

folder_name : str - The name of the folder where the inputs are stored

file_names : list | None - The names of the files to load (be aware that order matters
first file should be the inputs.conf file, second file should be the connections.conf file)
If None, defaults to [&#x27;db_inputs.conf&#x27;, &#x27;db_connections.conf&#x27;]

**Usage**:

```console
$ cribl-utilities-cli post-connections [OPTIONS] FOLDER_NAME
```

**Arguments**:

* `FOLDER_NAME`: [required]

**Options**:

* `--file-names TEXT`
* `--help`: Show this message and exit.

## `cribl-utilities-cli run-all`

Run all the commands in order (print_inputs_config, post_inputs, print_connections_config, post_connections)

folder_name : str - The name of the folder where the inputs are stored

file_names : list | None - The names of the files to load (be aware that order matters
first file should be the inputs.conf file, second file should be the connections.conf file)
If None, defaults to [&#x27;db_inputs.conf&#x27;, &#x27;db_connections.conf&#x27;]

save_trace_to_file : bool - If True, saves the trace to a file

**Usage**:

```console
$ cribl-utilities-cli run-all [OPTIONS] FOLDER_NAME
```

**Arguments**:

* `FOLDER_NAME`: [required]

**Options**:

* `--file-names TEXT`
* `--save-trace-to-file / --no-save-trace-to-file`: [default: no-save-trace-to-file]
* `--help`: Show this message and exit.
