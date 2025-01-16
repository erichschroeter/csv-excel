# CSV Excel

- [CSV Excel](#csv-excel)
  - [Feature comparison](#feature-comparison)
  - [Setting up the Virtual Environment](#setting-up-the-virtual-environment)
    - [Windows](#windows)
    - [Linux](#linux)
  - [Maintainers](#maintainers)

## Feature comparison

Some of the features may be arbitrary, but by using **csv-excel** it may be possible to have the best of both worlds.

| Feature             | Text Files                                           | Excel Files                                                       | Text Win | Excel Win |
|---------------------|------------------------------------------------------|-------------------------------------------------------------------|----------|-----------|
| Simplicity          | Easy to create and edit with basic text editors.     | Intuitive interface with user-friendly features.                  | X        |           |
| Version Control     | Works well with version control systems (e.g., Git). | Poor compatibility with version control due to binary format.     | X        |           |
| File Size           | Smaller file size for simple data structures.        | Can handle moderate data sizes with formatting.                   | X        |           |
| Portability         | Highly portable and platform-independent.            | Supported on most platforms with Excel readers.                   | X        |           |
| Data Organization   | Lacks inherent structure for tabular data.           | Designed for structured and tabular data.                         |          | X         |
| Data Validation     | No built-in validation or formatting.                | Built-in validation and formatting options.                       |          | X         |
| Usability           | Not user-friendly for non-technical users.           | Easy to navigate for users with minimal training.                 |          | X         |
| Scalability         | Becomes harder to manage with large datasets.        | Handles large datasets better with structured sheets.             |          | X         |
| Search and Sort     | Requires external tools.                             | Built-in search, sort, and filter features.                       |          | X         |
| Formatting          | Plain text only, no styling or formatting.           | Supports cell formatting, charts, and styles.                     |          | X         |
| Dependency          | Requires Excel software or compatible tools.         | Requires proprietary software or libraries to access.             | X        |           |
| Corruption Risk     | Low risk of file corruption.                         | Higher risk of file corruption, especially with complex files.    | X        |           |
| Complexity          | Simple structure is easy to debug and modify.        | Complex formatting and macros can complicate troubleshooting.     | X        |           |
| Automation          | Easily parsed with programming languages.            | Integrates well with tools like Python, VBA, etc.                 | X        |           |
| Automation Overhead | Minimal overhead for scripting and automation.       | Requires knowledge of Excel-specific automation (e.g., VBA).      | X        |           |
| Cost                | Free to use with no specialized software needed.     | May involve licensing costs for Excel software.                   | X        |           |

[top](#csv-excel)

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
