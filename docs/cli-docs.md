# `cribl-utilities-cli`

This is the main command line interface for the cribl-utilities CLI.

**Usage**:

```console
$ cribl-utilities-cli [OPTIONS] COMMAND [ARGS]...
```

**Options**:

* `--install-completion`: Install completion for the current shell.
* `--show-completion`: Show completion for the current shell, to copy it or customize the installation.
* `--help`: Show this message and exit.

**Commands**:

* `check-version`: Check the version of the cribl-utilities CLI.
* `example-env`: Print an example .env file.
* `check-cribl-health`: Check the health of the Cribl instance.
* `check-connection`: Check the connection to the Cribl instance.
* `print-inputs-config`: Load the inputs from the chosen folder.
* `post-inputs`: Post the inputs to the Cribl instance.
* `print-connections-config`: Load the connections from the examples folder.
* `post-connections`: Post the connections to the Cribl instance.
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

Print an example .env file.

**Usage**:

```console
$ cribl-utilities-cli example-env [OPTIONS]
```

**Options**:

* `--help`: Show this help message and exit.

## `cribl-utilities-cli check-cribl-health`

Check the health of the Cribl instance.

**Usage**:

```console
$ cribl-utilities-cli check-cribl-health [OPTIONS]
```

**Options**:

* `--help`: Show this help message and exit.

## `cribl-utilities-cli check-connection`

Check the connection to the Cribl instance.

**Usage**:

```console
$ cribl-utilities-cli check-connection [OPTIONS]
```

**Options**:

* `--help`: Show this help message and exit.

## `cribl-utilities-cli print-inputs-config`

Load the inputs from the chosen folder and print them to the console.

**Usage**:

```console
$ cribl-utilities-cli print-inputs-config [OPTIONS] FOLDER_NAME
```

**Arguments**:

* `FOLDER_NAME`: [required] (str)  
   The name of the folder where the inputs are stored.

**Options**:

* `--file-names TEXT`: (list | None)  
    A list of file names to load. The order of the files is important:  
    * The first file should be the inputs.conf file.  
    * The second file should be the connections.conf file.  
    * If no files are specified, the default is ['db_inputs.conf', 'db_connections.conf'].  
  
* `--help`: Show this help message and exit.  

## `cribl-utilities-cli post-inputs`

Post the inputs to the Cribl instance and print their ids to the console.  

**Usage**:

```console
$ cribl-utilities-cli post-inputs [OPTIONS] FOLDER_NAME
```

**Arguments**:

* `FOLDER_NAME`: [required] (str)  
   The name of the folder where the inputs are stored.

**Options**:

* `--file-names TEXT`: (list | None)  
    A list of file names to load. The order of the files is important:  
    * The first file should be the inputs.conf file.  
    * The second file should be the connections.conf file.  
    * If no files are specified, the default is ['db_inputs.conf', 'db_connections.conf'].  
  
* `--help`: Show this help message and exit.

## `cribl-utilities-cli print-connections-config`

Load the connections from the examples folder and print them to the console.

**Usage**:

```console
$ cribl-utilities-cli print-connections-config [OPTIONS] FOLDER_NAME
```

**Arguments**:

* `FOLDER_NAME`: [required] (str)  
   The name of the folder where the inputs are stored.

**Options**:

* `--file-names TEXT`: (list | None)  
    A list of file names to load. The order of the files is important:  
    * The first file should be the inputs.conf file.  
    * The second file should be the connections.conf file.  
    * If no files are specified, the default is ['db_inputs.conf', 'db_connections.conf'].  
* `--help`: 
  Show this help message and exit.

## `cribl-utilities-cli post-connections`

Post the connections to the Cribl instance and print their ids to the console.

**Usage**:

```console
$ cribl-utilities-cli post-connections [OPTIONS] FOLDER_NAME
```

**Arguments**:

* `FOLDER_NAME`: [required] (str)  
   The name of the folder where the inputs are stored.

**Options**:

* `--file-names TEXT`: (list | None)  
    A list of file names to load. The order of the files is important:  
    * The first file should be the inputs.conf file.  
    * The second file should be the connections.conf file.  
    * If no files are specified, the default is ['db_inputs.conf', 'db_connections.conf'].  
  
* `--help`: Show this help message and exit.

## `cribl-utilities-cli run-all`

Check the environment variables, Cribl health, get the Cribl auth token, load and post inputs and connections, and save the trace to a file.  

**Usage**:

```console
$ cribl-utilities-cli run-all [OPTIONS] FOLDER_NAME
```

**Arguments**:

* `FOLDER_NAME`: [required] (str)  
   The name of the folder where the inputs are stored.

**Options**:

* `--file-names TEXT`: (list | None)  
    A list of file names to load. The order of the files is important:  
    * The first file should be the inputs.conf file.  
    * The second file should be the connections.conf file.  
    * If no files are specified, the default is ['db_inputs.conf', 'db_connections.conf'].  
  
* `--save-trace-to-file / --no-save-trace-to-file`: [default: no-save-trace-to-file] (bool)
    If True, saves the trace to a file.

* `--help`: Show this help message and exit.
