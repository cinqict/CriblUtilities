# splunk-cribl-utilities
A python package, cli and docker image of function and classes that are useful for migrating from splunk to cribl.

## Initial goal
In the longer term this package/ application will encompass more functionality, however for the moment the goal is to convert splunk conf toml files to the format required by cribl and to send them via the cribl API.
To do this we will make:
1. a python package (with unit tests etc.) for the required function
2. using the python package we will make a simple cli
3. we will make a Docker image using the cli so people can easily use it without installing a bunch of stuff first

## To run
- Make sure to have installed a python version >=3.10
- `docker compose up -d`
  - login and update admin password (default is `admin` and `admin`)
- `pip install -r requirements.txt`
- `python example_usage.py`

## Cleanup
- `docker compose down`