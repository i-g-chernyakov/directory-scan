## directory-scan

# Directory Scanner

Periodically scans the defined directory and subdirectories up to the defined depth.

Stores information about files:
- path, 
- name, 
- extension, 
- size, 
- file mode, 
- owner/group, 
- access rights,
- time of creation,
- time of most recent content modification. 

Fixes changes in history:
- new files and directories,
- removed files and directories,
- changed files and directories.

 
# Getting Started 
 
## Installation

Install with `poetry` 

```bash 
  poetry install
```

Additional packages should be installed using extras 

```bash
  poetry install --extras "pgsql yaml"
```


## Config

The scanner can be configured by specifying command-line arguments or by 
configuration file. The configuration file can be in various formats. Some 
formats require to install additional packages:

| Format    |    Extras |  Requirement   |
|-----------|:----------|----------------|
| YAML      |   yaml    | ruamel.yaml    |
| ConfigObj | configobj | configobj      |
| TOML      | toml      | toml           |


When using database you need to install appropriated extras

| Database  |    Extras |  Requirement   |
|-----------|:----------|----------------|
| PostgreSQL|   pgsql   | psycopg2-binary|
| MySQL     | mysql     | mysqlclient    |


### config.yml
 
```yaml
# Recursive scan subdirectories to defined depth. Optional. 
# If not set than scan all subdirectories.
# Argument for command line --depth or -d
depth: 1

# Period of scanning. Optional. Default period is 60 seconds.
# Argument for command line --period or -p
period: 60

# Ignored extensions. Optional.
# By default ignored = ""
# Argument for command line --ignored or -i
ignored: ""

# Log level. Optional. 
# Default = "INFO"
# Argument for command line --log or -l
log_level: "DEBUG"

# Database url. Optional
# Argument for command line --database-url or -u
database_url: "postgresql+psycopg2://postgres:postgres@localhost/directory_scan"
```

### How to run
  
Example.

- With the configuration file:
```bash
  python directory_scan.py --config /path/to/config.yml /directory/to/scan
```
or
```bash
  python directory_scan.py -c /path/to/config.yml /directory/to/scan
```

- With command-line arguments:
```bash
  python directory_scan.py -p 60 -d 1 /directory/to/scan
```

Log to stdout and error to stderr  
