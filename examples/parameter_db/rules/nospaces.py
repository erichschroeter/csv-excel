import logging

def validate(workbook):
    for sheet in workbook.worksheets:
        logging.info(f'VALIDATING rule "no spaces" for sheet {sheet}')
