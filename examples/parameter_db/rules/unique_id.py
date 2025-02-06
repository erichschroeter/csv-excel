import logging
from csv_excel.csv_excel import RuleError, workbook_rule


@workbook_rule
def validate_unique_id(workbook):
    results = []
    if "Parameters" in workbook.sheetnames:
        sheet = workbook["Parameters"]
        ids = sheet["B"]
        ids = [cell.value for cell in ids]
        ids.sort()
        for i in set(ids):
            if ids.count(i) > 1:
                e = RuleError(__file__, f'not unique "{i}"')
                results.append(e)
                logging.error(f"Parameters: {e}")
    return results
