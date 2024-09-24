# simple example

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
