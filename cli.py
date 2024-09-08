import argparse
import csv
import os
from openpyxl import Workbook

def main(args):
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

        # Write the data to the worksheet
        for row in data:
            sheet.append(row)

    # Adjust column widths
    wb['Parameters'].column_dimensions['A'].width = 100

    # Delete the default sheet
    if 'Sheet' in wb.sheetnames:
        wb.remove(wb['Sheet'])
    # Save the workbook
    wb.save('output.xlsx')

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('csv_files', nargs='+', help='The CSV files to include in the Excel file')
    args = parser.parse_args()
    main(args)
