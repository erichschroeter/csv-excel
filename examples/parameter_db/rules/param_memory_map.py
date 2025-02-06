import logging
from csv_excel.csv_excel import WorkbookError, workbook_rule

COL_INDEX_ID = 0
SHEETNAME = "NV Memory"


@workbook_rule
def validate_param_id_exists(workbook):
    results = []
    ids = []
    if "Parameters" in workbook.sheetnames:
        ids = workbook["Parameters"]["B"]
        ids = [cell.value for cell in ids]
        ids.sort()
    if SHEETNAME in workbook.sheetnames:
        sheet = workbook[SHEETNAME]
        for rownum, id in enumerate(sheet["A"]):
            # Skip the CSV header
            if rownum == 0:
                continue
            if id.value not in ids:
                e = WorkbookError(
                    validate_param_id_exists.__name__,
                    SHEETNAME,
                    rownum + 1,
                    COL_INDEX_ID,
                    f'ID does not exist "{id.value}"',
                )
                results.append(e)
                logging.error(e)
    return results
