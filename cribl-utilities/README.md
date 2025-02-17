# Using the cribl-utilities-cli
## Install instructions
- `brew install pipx`
- `pipx install cribl-utilities`
- `cribl-utilities --help`

## Notes on usage
- Before running the CLI make sure that your variables file with the Cribl credentials are included in the same folder that you are running the CLI in. 
  - Use an existing variables file and use it running `source [FILE]`. To view an example or a variables file type cribl-utilities example-env
  - To create a new variables file use cribl-utilities setup. Use it running `source variables`