# CSV Excel

- [CSV Excel](#csv-excel)
  - [Setting up the Virtual Environment](#setting-up-the-virtual-environment)
    - [Windows](#windows)
    - [Linux](#linux)
  - [Maintainers](#maintainers)

## Setting up the Virtual Environment

1. Install `virtualenv` if you haven't already: `pip install virtualenv`

### Windows
```powershell
python -m venv .venv
. .venv\Scripts\activate
pip install -r requirements.txt
python -m csv-excel --help
```

[top](#csv-excel)

### Linux
```bash
python -m venv .venv
. .venv/bin/activate
pip install -r requirements.txt
git lfs pull
python -m csv-excel --help
```

[top](#csv-excel)

## Maintainers

See [DEVELOPERS.md](./DEVELOPERS.md)

[top](#csv-excel)
