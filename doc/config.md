# Configuration file

This document summarises all configuration options,
which are understood by the `libfulltext` suite.
Only some of these (marked *required*) are actually
required, the other ones are optional.

By default the scripts expect the configuration file at
`~/.config/libfulltext/config.yaml` ,
allthough this might be changed by appropriate commandline flags.

## Full configuration file skeleton
```yaml
# Fulltext document root storage directory
# (default: "./fulltext")
storage_fulltext: "relative_path_to_directory"

# Elsevier API key (required)
publishers_elsevier_apikey: "your_elsevier_api_key_here"
```
