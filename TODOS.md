## TODO list

- [ ] clean up our hardrives and make sure we have enough space to work (it would be way easier to be able to use Docker Desktop)
- [ ] create functions and add them to the ingestor class to post inputs.conf data to the Cribl API
- [ ] create functions and add them to the ingestor class to post authentication.conf data to the Cribl API
- [ ] research and choose a way to build the python package (**setup.py**, poetry, etc.) (https://packaging.python.org/tutorials/packaging-projects/)
- [ ] make a decision on how we will do unit tests (**pytest**, unittest, etc.)
- [ ] make a decision on what documentation we will use (**sphinx**, mkdocs, etc.)
- [ ] write unit tests for the ingestor class
- [ ] write documentation for the ingestor class (make sure your docstrings are good)
- [ ] create a cli (using Typer) that uses the ingestor class to post to the Cribl API
- [ ] create a Dockerfile that uses the cli to post to the Cribl API and publish it to Docker Hub