# parameter_db

- [parameter\_db](#parameter_db)
  - [File overview](#file-overview)
    - [`cli.py`](#clipy)
    - [`config.yml`](#configyml)
    - [`csv2xl.bat`](#csv2xlbat)
    - [`rules/`](#rules)
      - [`rules/nospaces.py`](#rulesnospacespy)
      - [`rules/param_memory_map.py`](#rulesparam_memory_mappy)
      - [`rules/unique_id.py`](#rulesunique_idpy)
    - [`worksheets/`](#worksheets)
      - [`worksheets/invalid/`](#worksheetsinvalid)
      - [`worksheets/valid/`](#worksheetsvalid)
  - [Running the example](#running-the-example)
    - [Windows](#windows)
    - [Linux](#linux)

This example shows how this project can be used to maintain a parameter database while avoiding Excel files in a source code repository.

## File overview
The project structure laid out for this project is just an example.
This project happens to store CSV files under the `worksheets/` folder and validation rules under the `rules/` folder, but could easily change those to other locations.
### `cli.py`
The CLI program containing `main` and parsing the command line.

[top](#parameter_db)

### `config.yml`
An example config file controlling how to generate an Excel file.
For example, if you wanted to increase the width of a column, you would specify that in here.
```yaml
sheets:
  Parameters:
    columns:
      A:
        width: 25
```

[top](#parameter_db)

### `csv2xl.bat`
An example batch script to execute the `csv2xl` subcommand.
This is useful for people that don't know how to use the command line in Windows.

The script will create an Excel file named `worksheets/valid/db.xlsm` and use the `config.yml` configuration file.

[top](#parameter_db)

### `rules/`
#### `rules/nospaces.py`
An example rule to check that parameter names do not contain spaces.

[top](#parameter_db)

#### `rules/param_memory_map.py`
An example rule to check that each parameter in the `NV Memory.csv` exists within `Parameters.csv`

[top](#parameter_db)

#### `rules/unique_id.py`
An example rule to check that each parameter ID in the `Parameters.csv` is unique.

[top](#parameter_db)

### `worksheets/`
#### `worksheets/invalid/`
An example with invalid CSV files to show validation errors with `worksheets/invalid/Parameters.csv` and `worksheets/invalid/NV Memory.csv` files.
```
$ python cli.py validate --rules_dir rules/ worksheets/invalid/*
2024-10-22 10:46:42,989 - ERROR - nospaces.py: (row: 1, col: 1): invalid C++ identifier "PARAM Y"
2024-10-22 10:46:42,989 - ERROR - param_memory_map.py: (row: 2, col: 1): ID does not exist "PARAM_E"
2024-10-22 10:46:42,989 - ERROR - unique_id.py: not unique "PARAM_X"
```

[top](#parameter_db)

#### `worksheets/valid/`
An example with valid CSV files to correctly generate an Excel file with `worksheets/valid/Parameters.csv` and `worksheets/valid/NV Memory.csv` files.

Generate an Excel file from CSV files:
```bash
python cli.py csv2xl -o worksheets/valid/db.xlsm worksheets/valid/*.csv
```

Update CSV files based on changes made within an Excel file:
```bash
python cli.py xl2csv -o worksheets/valid/ worksheets/valid/db.xlsm
```

[top](#parameter_db)

## Running the example

### Windows

```powershell
python -m venv .venv
. .venv\Scripts\activate
pip install -r requirements.txt
git lfs pull
python cli.py
```

### Linux

> [!NOTE]
> The bash code below is written with the intent to be executed from the top level git directory.

```bash
python -m venv .venv
. .venv/bin/activate
pip install -r requirements.txt
git lfs pull
python examples/parameter_db/cli.py -c examples/parameter_db/config.yml csv2xl examples/parameter_db/worksheets/valid/*.csv
```

[top](#parameter_db)
