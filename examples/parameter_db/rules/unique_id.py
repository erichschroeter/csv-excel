
def validate(workbook):
    print(f'VALIDATING : {workbook.filename} for rule "unique id"')
    for sheet in workbook.worksheets():
        if 'Parameters' == sheet.name:
            for row in sheet.table:
                print(f'{row}')
