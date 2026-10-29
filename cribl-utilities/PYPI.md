# cribl-utilities

A command-line tool for migrating to [Cribl Stream](https://cribl.io/stream/) and validating Cribl configurations.

- **Migrate Splunk DB Connect to Cribl.** Converts your Splunk DB Connect configuration into Cribl database connections and database collector sources, and creates them in Cribl through its API.
- **Validate Cribl configuration in GitOps workflows.** Checks YAML syntax and naming conventions in a `cribl-config` folder, so problems are caught before changes are deployed.

## Installation

Requires Python 3.12 or later. Installing with [pipx](https://pipx.pypa.io/) is recommended:

```bash
brew install pipx        # or see pipx docs for other platforms
pipx install cribl-utilities
cribl-utilities --help
```

## Configuration

The CLI reads its settings from environment variables in your current shell.

Create a `variables` file interactively and load it:

```bash
cribl-utilities setup
source variables
```

Or write your own file (run `cribl-utilities example-env` for a template) and load it with `source <file>`.

| Variable | Required | Description |
|---|---|---|
| `CRIBL_USERNAME` | yes | Cribl user name |
| `CRIBL_PASSWORD` | yes | Cribl password |
| `BASE_URL` | yes | URL of the Cribl leader, e.g. `http://localhost:19000` |
| `CRIBL_WORKERGROUP_NAME` | yes | Worker group to create the connections and sources in |
| `DBCONN_PREFIX` / `DBCONN_SUFFIX` | no | Prefix / suffix for database connection IDs. Use `{guid}` as suffix for a unique ID |
| `DBCOLL_PREFIX` / `DBCOLL_SUFFIX` | no | Prefix / suffix for database collector source IDs. Use `{guid}` as suffix for a unique ID |
| `SCHEDULE_ENABLED` | no | Set to `false` to create all collector schedules disabled. Default: `true` |

Verify the setup:

```bash
cribl-utilities check env            # environment variables are set
cribl-utilities check cribl-health   # Cribl is reachable
cribl-utilities check connection     # credentials work
```

## Migrating Splunk DB Connect

Copy the DB Connect configuration files from your Splunk instance into one folder:

| File | Required | Contents |
|---|---|---|
| `db_inputs.conf` | yes | Database inputs, become Cribl database collector sources |
| `db_connections.conf` | yes | Database connections, become Cribl database connections |
| `identities.conf` | no | Credentials. Not needed when credentials are in the connection string |

Preview the result without changing anything in Cribl:

```bash
cribl-utilities print-connections-config <folder>
cribl-utilities print-inputs-config <folder>
```

Then create everything in Cribl:

```bash
cribl-utilities migrate-database <folder>
```

Add `--save-trace-to-file` to write the loaded configuration and the Cribl API responses to `trace.txt`. Use `post-connections` and `post-inputs` to create only one of the two.

How the configuration is translated:

- **Schedules:** a disabled Splunk input (`disabled = 1` or `true`) gets a disabled schedule in Cribl. Intervals in seconds are converted to cron expressions.
- **Database types:** Oracle, Microsoft SQL Server (including Windows authentication) and PostgreSQL are supported. DB2, Sybase ASE and Vertica are not supported yet.

## Validating Cribl configuration

Check that the YAML files in a `cribl-config` folder are valid:

```bash
cribl-utilities check files --conf <cribl-config folder>
```

Check that names follow a naming convention:

```bash
cribl-utilities check naming --conf <cribl-config folder> --field sources --regex '^src_[a-z0-9_]+$'
```

`--field` is one of `workergroup`, `sources`, `destinations`, `dataroutes`, `pipelines` or `packs`. Use `--exceptions` to skip specific names.

Run `cribl-utilities <command> --help` for all options of a command.

## License

Apache License 2.0. Developed by [CINQ ICT](https://www.cinqict.nl).
