CriblUtilities is a Python CLI package that streamlines migration to Cribl Stream and validates configurations. With minimal setup, it transfers configurations from existing tools to Cribl Stream. It also integrates with Cribl GitOps workflows to verify naming conventions and file formats before implementing changes.

# Using cribl-utilities CLI
## Install instructions
- `brew install pipx`
- `pipx install cribl-utilities`
- `cribl-utilities --help`

## Notes on usage
- Before running the CLI make sure that your variables file with the Cribl credentials are included in the same folder that you are running the CLI in. 
  - To create a new variables file run `cribl-utilities setup`. Use the generated variables file running `source variables`
  - Use an existing variables file and use it running `source [FILE]`. To view an example or a variables file type cribl-utilities example-env
