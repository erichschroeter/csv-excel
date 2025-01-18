@echo off

@REM Description: Convert CSV files to Excel file.

@REM Activate the Python virtual environment if it exists, otherwise create it.
IF EXIST .venv (
    call .venv\Scripts\activate.bat
) ELSE (
    python -m venv .venv
    call .venv\Scripts\activate.bat
    pip install -r requirements.txt
)

@REM Use a for loop to glob all CSV files into a variable to pass to the Python program.
setlocal enableDelayedExpansion
set CSV_FILES=
for %%f in (worksheets\valid\*.csv) do set CSV_FILES=!CSV_FILES! "%%f"

python cli.py -c config.yml csv2xl -o worksheets\valid\db.xlsm %CSV_FILES%

@REM Uncomment the `pause` below for debugging.
@REM pause