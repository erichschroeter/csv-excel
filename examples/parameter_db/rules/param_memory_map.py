import logging

from csv_excel.csv_excel import CsvRuleError


def validate(workbook):
    results = []
    ids = []
    if "Parameters" in workbook.sheetnames:
        ids = workbook["Parameters"]["B"]
        ids = [cell.value for cell in ids]
        ids.sort()
    if "NV Memory" in workbook.sheetnames:
        sheet = workbook["NV Memory"]
        for rownum, id in enumerate(sheet["A"]):
            # Skip the CSV header
            if rownum == 0:
                continue
            if id.value not in ids:
                results.append(
                    CsvRuleError(__file__, rownum, 1, f'ID does not exist "{id.value}"')
                )
    return results
