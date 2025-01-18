@echo off

@REM Description: Validate CSV files based on the rules within the `rules/` directory.

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
for %%f in (worksheets\invalid\*.csv) do set CSV_FILES=!CSV_FILES! "%%f"

python cli.py -c config.yml validate --rules_dir rules\ %CSV_FILES%

@REM Keep the command prompt open for viewing the validation output.
pause