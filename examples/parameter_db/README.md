# parameter_db example

- [parameter\_db example](#parameter_db-example)
  - [Files](#files)
    - [`cli.py`](#clipy)
    - [`config.yml`](#configyml)
    - [`rules/`](#rules)
      - [`rules/nospaces.py`](#rulesnospacespy)
      - [`rules/param_memory_map.py`](#rulesparam_memory_mappy)
      - [`rules/unique_id.py`](#rulesunique_idpy)
    - [`worksheets/`](#worksheets)
      - [`worksheets/invalid/`](#worksheetsinvalid)
      - [`worksheets/valid/`](#worksheetsvalid)
  - [Setting up the Virtual Environment](#setting-up-the-virtual-environment)
    - [Windows](#windows)
    - [Linux](#linux)

This example shows how this project can be used to maintain a parameter database while avoiding Excel files in a source code repository.

|Advantages|Disadvantages|
|----|----|
|CSV is easy to update (with Excel or text editor)|Maintainers will need to generate Excel file with this script|
|CSV is diffable (mergable with Git)||
|Can modify DB in Windows or Linux||
|Can maintain validation logic in Python||

## Files
The project structure laid out for this project is just an example.
This project happens to store CSV files under the `worksheets/` folder and validation rules under the `rules/` folder, but could easily change those to other locations.
### `cli.py`
The CLI program containing `main` and parsing the command line.
### `config.yml`
An example config file controlling how to generate an Excel file.
### `rules/`
#### `rules/nospaces.py`
An example rule to check that parameter names do not contain spaces.
#### `rules/param_memory_map.py`
An example rule to check that each parameter in the `NV Memory.csv` exists within `Parameters.csv`
#### `rules/unique_id.py`
An example rule to check that each parameter ID in the `Parameters.csv` is unique.
### `worksheets/`
#### `worksheets/invalid/`
An example CSV file to show validation errors with `worksheets/invalid/Parameters.csv` and `worksheets/invalid/NV Memory.csv` files.
```
$ python cli.py validate --rules_dir rules/ worksheets/invalid/*
2024-10-22 10:46:42,989 - ERROR - nospaces.py: (row: 1, col: 1): invalid C++ identifier "PARAM Y"
2024-10-22 10:46:42,989 - ERROR - param_memory_map.py: (row: 2, col: 1): ID does not exist "PARAM_E"
2024-10-22 10:46:42,989 - ERROR - unique_id.py: not unique "PARAM_X"
```
#### `worksheets/valid/`
An example CSV file to correctly generate an Excel file with `worksheets/valid/Parameters.csv` and `worksheets/valid/NV Memory.csv` files.

Generate an Excel file from CSV files:
```bash
python cli.py csv2xl -o worksheets/valid/db.xlsm worksheets/valid/*.csv
```

Update CSV files based on changes made within an Excel file:
```bash
python cli.py xl2csv -o worksheets/valid/ worksheets/valid/db.xlsm
```

## Setting up the Virtual Environment

1. Install `virtualenv` if you haven't already: `pip install virtualenv`

### Windows
```powershell
python -m venv .venv
. .venv\Scripts\activate
pip install -r requirements.txt
python cli.py
```

### Linux
```bash
python -m venv .venv
. .venv/bin/activate
pip install -r requirements.txt
python cli.py
```
