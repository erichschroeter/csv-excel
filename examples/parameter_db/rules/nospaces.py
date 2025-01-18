import re

from csv_excel.csv_excel import CsvRuleError, RuleError

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
