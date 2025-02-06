import logging
from csv_excel.csv_excel import WorkbookError, workbook_rule


@workbook_rule
def validate_unique_id(workbook):
    SHEETNAME = "Parameters"
    results = []
    if SHEETNAME in workbook.sheetnames:
        sheet = workbook[SHEETNAME]
        ids = sheet["B"]
        ids = [cell.value for cell in ids]
        ids.sort()
        for i in set(ids):
            if ids.count(i) > 1:
                e = WorkbookError(
                    validate_unique_id.__name__, SHEETNAME, 0, 0, f'not unique "{i}"'
                )
                results.append(e)
                logging.error(e)
    return results
