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
- [✓] Error handling and unit tests for the ingestor class. Consider:  
        - [✓] environment variables set (right)  
        - [✓] connection to Cribl  
        - [✓] validation of input files: 3 files, right format  
        - [✓] warning if username, password, or domain are missing.
        - [✓] validation of input path and input file names
        - [✓] in each field throw error in case of data type mismatch 
- [ ] Make optional parameter to overwrite schedule.enable to false for all
- [✓] write documentation for the ingestor class (make sure your docstrings are good)
- [✓] create a cli (using Typer) that uses the ingestor class to post to the Cribl API
- [ ] create a Dockerfile that uses the cli to post to the Cribl API and publish it to Docker Hub
- [✓] CLI command 'cribl-utilities-cli migrate-database': 
  - does the same as the current run-all
- [ ] re structure cli  to move the commands out of main.py into separate modules (e.g., commands/), so we use commands and subcommands add in main:  
      app.add_typer(command1.app, name="command1")  
      cribl-utilities-cli command1 function1]
- [ ] CLI command 'cribl-utilities-cli environmentvalues -key value':
  - Remove the dotenv import and function call
  - Windows: for /f "tokens=1,2 delims==" %i in (my_env_file.txt) do set %i=%j
  python script.py
  -  macOS/Linux: source my_env_file.txt (export command)
- [ ] CLI command 'cribl-utitilies-cli setup': add env variables manually one by one
- [ ] CLI command 'cribl-utilities-check-files': checks if expected files are adhering to YAML linting. Basic sintax validation
- [ ] CLI command 'cribl-utilities-cli check-naming -conf': see docs. Check regex naming convention.
- 
