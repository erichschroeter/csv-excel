import logging
from csv_excel.csv_excel import CsvRuleError, workbook_rule

COL_INDEX_ID = 0


@workbook_rule
def validate_param_id_exists(workbook):
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
                e = CsvRuleError(
                    __file__,
                    rownum + 1,
                    COL_INDEX_ID,
                    f'ID does not exist "{id.value}"',
                )
                results.append(e)
                logging.error(f"NV Memory: {e}")
    return results
