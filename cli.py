import argparse
import csv
import logging
import os
import yaml
from openpyxl import Workbook

def main(args):
    config = None
    if args.config:
        with open(args.config, 'r') as yamlfile:
            config = yaml.safe_load(yamlfile)
            # for key, value in config.items():
            #     print(f"{key}: {value}")

    # Create a new workbook
    wb = Workbook()

    # Iterate over each CSV file
    for csv_file in args.csv_files:
        # Load the CSV file
        with open(csv_file, 'r') as f:
            reader = csv.reader(f)
            data = list(reader)

        # Create a new worksheet for this CSV file
        clean_title = os.path.basename(csv_file)  # don't inclue full path, just file name
        clean_title = os.path.splitext(clean_title)[0]  # remove extension
        sheet = wb.create_sheet(title=clean_title)

        if config:
            if clean_title in config['sheets']:
                sheet_config = config['sheets'][clean_title]
                if 'columns' in sheet_config:
                    for colname, colcfg in sheet_config['columns'].items():
                        if 'width' in colcfg:
                            logging.debug(f'Setting column "{colname}" to width of {colcfg["width"]}')
                            sheet.column_dimensions[colname].width = int(colcfg['width'])

        # Write the data to the worksheet
        for row in data:
            sheet.append(row)

    # Delete the default sheet
    if 'Sheet' in wb.sheetnames:
        wb.remove(wb['Sheet'])
    # Save the workbook
    wb.save('output.xlsx')

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('csv_files', nargs='+', help='The CSV files to include in the Excel file')
    parser.add_argument('-c', '--config', help='YAML config file')
    args = parser.parse_args()
    main(args)
