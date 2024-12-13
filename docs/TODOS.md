## TODO list

- [✓] clean up our hardrives and make sure we have enough space to work (it would be way easier to be able to use Docker Desktop)
- [✓] Adjust schemas, create functions, and integrate them into the ingestor class to post the mapped data to the Cribl Input API.
- [✓] Adjust schemas, create functions, and integrate them into the ingestor class to post the mapped data to the Cribl Connections API.
- [✓] research and choose a way to build the python package (**setup.py**, poetry, etc.) (https://packaging.python.org/tutorials/packaging-projects/)  
    To build and manage a package, use poetry. Automated environment and dependencies management. Integrated publishing to PyPi.  
    If we want to share a standalone executable that works in any system without having to install pyton, use PyInstaller.  
- [✓] make a decision on how we will do unit tests (**pytest**, unittest, etc.)
- [✓] make a decision on what documentation we will use (**sphinx**, mkdocs, etc.)  
MkDocs is free and easy to use. It is a static site generator that's geared towards project documentation. It is simple to configure and use, and it is also easy to customize.
- [ ] Error handling and unit tests for the ingestor class. Consider:  
        - [✓] environment variables set (right)  
        - [✓] connection to Cribl  
        - [ ] validation of input files: 3 files, right format  
        - [✓] warning if username, password, or domain are missing.
        - [✓] validation of input path and input file names
        - [ ] in each field throw error in case of data type mismatch 
- [ ] Make optional parameter to overwrite schedule.enable to false for all
- [ ] write documentation for the ingestor class (make sure your docstrings are good)
- [✓] create a cli (using Typer) that uses the ingestor class to post to the Cribl API
- [ ] create a Dockerfile that uses the cli to post to the Cribl API and publish it to Docker Hub