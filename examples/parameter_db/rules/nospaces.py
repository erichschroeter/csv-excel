import re

from csv_excel.csv_excel import CsvRuleError, RuleError
from csv_excel.csv_excel import worksheet_rule

CPP_IDENTIFIER_REGEX = r"^[a-zA-Z_]+[a-zA-Z0-9_]*$"
CPP_IDENTIFIER_PATTERN = re.compile(CPP_IDENTIFIER_REGEX)


def validate(workbook) -> list[RuleError]:
    results = []
    if "Parameters" in workbook.sheetnames:
        sheet = workbook["Parameters"]
        for rownum, id in enumerate(sheet["B"]):
            # Skip the CSV header
            if rownum == 0:
                continue
            if not CPP_IDENTIFIER_PATTERN.fullmatch(id.value):
                results.append(
                    CsvRuleError(
                        __file__, rownum, 1, f'invalid C++ identifier "{id.value}"'
                    )
                )
    return results


@csv_data_rule(applies_to=["Parameters.csv"])
def validate_variable_contains_no_spaces(row_data, row_num):
    if not CPP_IDENTIFIER_PATTERN.fullmatch(row_data["Code"]):
        raise CsvRuleError(
            __file__, row_num, 1, f'invalid C++ identifier "{row_data["Code"]}"'
        )


@worksheet_rule(sheets=["Parameters.csv"])
def validate_variable_contains_no_spaces(reader):
    # Skip the CSV header
    next(reader)
    results = []
    for line in reader:
        if not CPP_IDENTIFIER_PATTERN.fullmatch(line[1]):
            results.append(
                CsvRuleError(
                    __file__, reader.line_num, 1, f'invalid C++ identifier "{line[1]}"'
                )
            )
    return results
