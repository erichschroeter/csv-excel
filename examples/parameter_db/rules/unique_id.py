
from csv_excel.csv_excel import RuleError


def validate(workbook) -> list[RuleError]:
    results = []
    if 'Parameters' in workbook.sheetnames:
        sheet = workbook['Parameters']
        ids = sheet['B']
        ids = [cell.value for cell in ids]
        ids.sort()
        for i in set(ids):
            if ids.count(i) > 1:
                results.append(RuleError(__file__, f'not unique "{i}"'))
    return results
