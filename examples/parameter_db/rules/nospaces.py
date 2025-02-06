import logging
import re

from csv_excel.csv_excel import CsvRuleError, csv_data_rule

COL_INDEX_ID = 1
CPP_IDENTIFIER_REGEX = r"^[a-zA-Z_]+[a-zA-Z0-9_]*$"
CPP_IDENTIFIER_PATTERN = re.compile(CPP_IDENTIFIER_REGEX)


@csv_data_rule(applies_to=["Parameters.csv", "NV Memory.csv"])
def validate_variable_contains_no_spaces(row_data, row_num):
    if not CPP_IDENTIFIER_PATTERN.fullmatch(row_data["ID"]):
        e = CsvRuleError(
            __file__,
            row_num + 1,
            COL_INDEX_ID,
            f'invalid C++ identifier "{row_data["ID"]}"',
        )
        logging.error(e)
