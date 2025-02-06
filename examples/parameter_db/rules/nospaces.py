import logging
import re

from csv_excel.csv_excel import CsvDataError, csv_data_rule

COL_INDEX_ID = 1
CPP_IDENTIFIER_REGEX = r"^[a-zA-Z_]+[a-zA-Z0-9_]*$"
CPP_IDENTIFIER_PATTERN = re.compile(CPP_IDENTIFIER_REGEX)


@csv_data_rule(applies_to=["Parameters.csv", "NV Memory.csv"])
def validate_variable_contains_no_spaces(file_path, row_data, row_num):
    results = []
    if not CPP_IDENTIFIER_PATTERN.fullmatch(row_data["ID"]):
        e = CsvDataError(
            validate_variable_contains_no_spaces.__name__,
            file_path,
            row_num + 1,
            COL_INDEX_ID,
            f'invalid C++ identifier "{row_data["ID"]}"',
        )
        results.append(e)
        logging.error(e)
    return results
