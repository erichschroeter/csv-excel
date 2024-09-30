
import logging


def validate(workbook):
    for sheet in workbook.worksheets:
        logging.info(f'VALIDATING rule "unique id" for sheet {sheet}')
    # for sheet in workbook.worksheets():
    #     if 'Parameters' == sheet.name:
    #         for row in sheet.table:
    #             print(f'{row}')
