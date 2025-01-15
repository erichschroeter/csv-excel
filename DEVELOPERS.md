# Developers

- [Developers](#developers)
  - [Design](#design)
  - [Developing](#developing)
    - [Install package locally for developing](#install-package-locally-for-developing)
    - [Update pypi version](#update-pypi-version)
    - [Executing unit tests](#executing-unit-tests)

## Design

```mermaid
---
title: Components
---
flowchart LR
    config --> Python
    rules --> Python
    worksheets --> Python
    Python --> Excel
```

## Developing

### Install package locally for developing

```bash
pip uninstall -y erichschroeter.csv-excel
python3 -m build
pip install dist/erichschroeter.csv_excel-0.1.0-py3-none-any.whl
```

[top](#developers)

### Update pypi version

```bash
python3 -m build
python3 -m twine upload --repository testpypi dist/*
```

[top](#developers)

### Executing unit tests
The following command will execute the unit tests.

```bash
python -m unittest
```

or, using [pytest](https://docs.pytest.org/en/6.2.x/):

```bash
python -m venv .venv
. .venv/bin/activate
pip install -r requirements-dev.txt
python -m pytest
```

[top](#developers)
