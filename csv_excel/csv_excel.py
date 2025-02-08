import csv
import glob
import importlib
import importlib.util
import inspect
import json
import logging
import time
import openpyxl
from openpyxl.styles import Font, PatternFill
import os
from os.path import dirname, basename, isfile, join
from pathlib import Path
import xlsxwriter
from xlsxwriter.utility import xl_cell_to_rowcol
import yaml


def column_to_index(col_str):
    """
    Convert a column cell reference notation to a zero indexed row and column.
    For example, 'A' will assume 'A1' and return (0,0)

    Args:
       col_str:  The column for A1 style string.

    Returns:
        row, col: Zero indexed cell row and column indices.

    """
    return xl_cell_to_rowcol(f"{col_str.upper()}1")[1]


class RuleError(Exception):
    pass


class CsvDataError(RuleError):
    def __init__(self, rule, filename, row, col, message):
        super().__init__(
            f"{rule} -- file: '{filename}', row: {row}, col: {col} --> {message}"
        )


class WorkbookError(RuleError):
    def __init__(self, rule, sheet, row, col, message):
        super().__init__(
            f"{rule} -- sheet: '{sheet}': row: {row}, col: {col} --> {message}"
        )


def read_config(config_path):
    with open(config_path, "r") as yamlfile:
        logging.debug(f"Loading config: {config_path}")
        return yaml.safe_load(yamlfile)


class ExcelStrategy:
    def create_workbook(self):
        raise NotImplementedError

    def add_worksheet(self, workbook, name):
        raise NotImplementedError

    def create_format(self, workbook, **kwargs):
        raise NotImplementedError

    def write_data(self, worksheet, row, col, data, cell_format):
        raise NotImplementedError

    def save(self, workbook, filename):
        raise NotImplementedError


class XlsxWriterStrategy(ExcelStrategy):
    def create_workbook(self):
        return xlsxwriter.Workbook()

    def add_worksheet(self, workbook, name):
        return workbook.add_worksheet(name)

    def create_format(self, workbook, **kwargs):
        return workbook.add_format(kwargs)

    def write_data(self, worksheet, row, col, data, cell_format):
        worksheet.write(row, col, data, cell_format)

    def save(self, workbook, filename):
        workbook.close()


class OpenPyxlStrategy(ExcelStrategy):
    def create_workbook(self):
        return openpyxl.Workbook()

    def add_worksheet(self, workbook, name):
        return workbook.create_sheet(title=name)

    def create_format(self, workbook, **kwargs):
        cell_format = {}
        if "font_color" in kwargs:
            cell_format["font"] = Font(color=kwargs["font_color"])
        if "bg_color" in kwargs:
            cell_format["fill"] = PatternFill(
                start_color=kwargs["bg_color"],
                end_color=kwargs["bg_color"],
                fill_type="solid",
            )
        return cell_format

    def write_data(self, worksheet, row, col, data, cell_format):
        cell = worksheet.cell(row=row + 1, column=col + 1, value=data)
        if cell_format:
            if "font" in cell_format:
                cell.font = cell_format["font"]
            if "fill" in cell_format:
                cell.fill = cell_format["fill"]

    def save(self, workbook, filename):
        workbook.save(filename)


class ExcelWorkbook:
    def __init__(self, strategy: ExcelStrategy):
        self.strategy = strategy
        self.workbook = self.strategy.create_workbook()
        self.worksheets = {}
        self.formats = {}

    def add_worksheet(self, name=None):
        worksheet = self.strategy.add_worksheet(self.workbook, name)
        self.worksheets[name] = worksheet
        return worksheet

    def create_format(self, **kwargs):
        cell_format = self.strategy.create_format(self.workbook, **kwargs)
        self.formats[tuple(kwargs.items())] = cell_format
        return cell_format

    def write_data(self, worksheet_name, row, col, data, cell_format=None):
        worksheet = self.worksheets.get(worksheet_name)
        if not worksheet:
            raise ValueError(f"Worksheet {worksheet_name} does not exist.")
        self.strategy.write_data(worksheet, row, col, data, cell_format)

    def save(self, filename):
        self.strategy.save(self.workbook, filename)


class WorkbookFactory:
    def __init__(self, config=None, csv_files=[]) -> None:
        # To support testability, provide a way to override config handlers.
        self.handlers = {
            "set_column_width": self._set_column_width,
            "set_row_height": self._set_row_height,
            "set_freeze_panes": self._set_freeze_panes,
        }
        self.config_path = None
        self.config = config
        self.csv_data_readers = csv_files

    def with_config(self, config_path):
        self.config_path = config_path
        with open(self.config_path, "r") as yamlfile:
            logging.debug(f"Loading config: {self.config_path}")
            self.config = yaml.safe_load(yamlfile)
        return self

    def with_csv_files(self, csv_file_paths):
        return self

    def _csv_path_to_worksheet_title(self, csv_path) -> str:
        title = os.path.basename(csv_path)  # don't include full path, just file name
        title = os.path.splitext(title)[0]  # remove extension
        return title

    def _set_column_width(self, sheet, column_name, width):
        colindex = column_to_index(column_name)
        logging.debug(
            f'Sheet "{sheet.get_name()}" column "{column_name}" ({colindex}) to {width}px'
        )
        sheet.set_column_pixels(colindex, colindex, width)

    def _set_row_height(self, sheet, rowidx, height_pixels=20, format=None):
        logging.debug(f'Sheet "{sheet.get_name()}" row "{rowidx}" to {height_pixels}px')
        sheet.set_row_pixels(rowidx, height_pixels, format)

    def _set_freeze_panes(self, sheet, rowindex, colindex):
        logging.debug(
            f'Sheet "{sheet.get_name()}" freezing row "{rowindex}" column "{colindex}"'
        )
        sheet.freeze_panes(rowindex, colindex)

    def build_openpyxl(self, csv_files, output_path=None):
        wb = openpyxl.Workbook()
        # Delete the default sheet
        if "Sheet" in wb.sheetnames:
            wb.remove(wb["Sheet"])
        for csv_file in csv_files:
            with open(csv_file, "r") as f:
                reader = csv.reader(f)
                csv_data = list(reader)

            worksheet_title = self._csv_path_to_worksheet_title(csv_file)
            sheet = wb.create_sheet(title=worksheet_title)
            logging.debug(f'Added worksheet "{worksheet_title}"')

            # Write the data to the worksheet
            for data in csv_data:
                sheet.append(data)
        if output_path:
            wb.save(output_path)
        return wb

    def build_xlsxwriter(self, csv_files, output_path):
        wb = xlsxwriter.Workbook(output_path)
        # Delete the default sheet
        if "Sheet" in wb.sheetnames:
            wb.remove(wb["Sheet"])
        # Include the Excel macro that auto exports worksheets to CSV files when file is saved.
        vbaproject_path = f"{os.path.dirname(os.path.abspath(__file__))}/vbaProject.bin"
        logging.debug(f'Packing VBA project into Excel file: "{vbaproject_path}"')
        wb.add_vba_project(vbaproject_path)

        start_time = time.time()
        for csv_file in csv_files:
            worksheet_title = self._csv_path_to_worksheet_title(csv_file)
            sheet = wb.add_worksheet(name=worksheet_title)
            logging.debug(f'Added worksheet "{worksheet_title}"')

            # Configuration scenarios
            # 1. No config file
            # 2. Entire col
            # 3. Entire row
            # 4. Entire col & row
            # 5. Specific cell

            # Apply any config specifications.
            if self.config:
                logging.warning(self.config)
                if worksheet_title in self.config["sheets"]:
                    sheet_config = self.config["sheets"][worksheet_title]
                    if "rows" in sheet_config:
                        for rowidx, rowcfg in sheet_config["rows"].items():
                            if "height" in rowcfg and "format" in rowcfg:
                                fmt = wb.add_format(rowcfg["format"])
                                self.handlers["set_row_height"](
                                    sheet, rowidx, int(rowcfg["height"]), fmt
                                )
                            elif "height" in rowcfg:
                                self.handlers["set_row_height"](
                                    sheet, rowidx, int(rowcfg["height"])
                                )
                            elif "format" in rowcfg:
                                fmt = wb.add_format(rowcfg["format"])
                                self.handlers["set_row_height"](
                                    sheet=sheet, rowidx=rowidx, format=fmt
                                )
                    if "columns" in sheet_config:
                        for colname, colcfg in sheet_config["columns"].items():
                            if "width" in colcfg:
                                self.handlers["set_column_width"](
                                    sheet, colname, int(colcfg["width"])
                                )
                    if (
                        "freeze_pane_row" in sheet_config
                        and "freeze_pane_col" in sheet_config
                    ):
                        row = sheet_config["freeze_pane_row"]
                        col = sheet_config["freeze_pane_col"]
                        self.handlers["set_freeze_panes"](sheet, row, col)
                    elif "freeze_pane_row" in sheet_config:
                        row = sheet_config["freeze_pane_row"]
                        self.handlers["set_freeze_panes"](sheet, row, 0)
                    elif "freeze_pane_col" in sheet_config:
                        col = sheet_config["freeze_pane_col"]
                        self.handlers["set_freeze_panes"](sheet, 1, col)

            with open(csv_file, "r") as f:
                reader = csv.reader(f)
                for rowidx, row in enumerate(reader):
                    for colidx, cell in enumerate(row):
                        sheet.write(rowidx, colidx, cell)
        end_time = time.time()
        elapsed_time_ms = (end_time - start_time) * 1_000
        logging.info(f"Elapsed time: {elapsed_time_ms} ms")

        return wb


def csv2xl(args):
    """
    Generates or updates an Excel file from multiple CSV files.

    Args:
        args:  The command line args.
    """
    # Use xlsxwriter due to support for vbaProject macros.
    wb = (
        WorkbookFactory()
        .with_config(args.config)
        .build_xlsxwriter(args.csv_files, args.output)
    )
    # Save the workbook
    wb.close()


def xl2csv(args):
    """
    Exports worksheets within an Excel file to CSV files.

    Args:
        args:  The command line args.
    """
    wb = openpyxl.load_workbook(args.file)
    # Create the output directory if it does not exist.
    if args.output_dir:
        Path(args.output_dir).mkdir(parents=True, exist_ok=True)
    for sheet in wb:
        with open(
            os.path.join(
                args.output_dir if args.output_dir else "", f"{sheet.title}.csv"
            ),
            "w+",
            newline="",
            encoding="utf-8",
        ) as f:
            logging.debug(f'Exporting worksheet "{sheet.title}"')
            c = csv.writer(f)
            for row in sheet.rows:
                c.writerow([cell.value for cell in row])


def collect_csv_data_rules(file_path):
    """
    Reads the file for functions annotated with @csv_data_rule.
    """
    # Load the modules from the file path
    spec = importlib.util.spec_from_file_location("temp_module", file_path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)

    # Collect all the functions annotated with @csv_data_rule
    rules = []
    for _, obj in inspect.getmembers(module, inspect.isfunction):
        if hasattr(obj, "_is_csv_data_rule") and obj._is_csv_data_rule:
            logging.debug(f"Found csv_data_rule in {file_path}: {obj.__name__}")
            rules.append(obj)
    return rules


def collect_workbook_rules(file_path):
    """
    Reads the file for functions annotated with @workbook_rule.
    """
    # Load the modules from the file path
    spec = importlib.util.spec_from_file_location("temp_module", file_path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)

    # Collect all the functions annotated with @workbook_rule
    rules = []
    for _, obj in inspect.getmembers(module, inspect.isfunction):
        if hasattr(obj, "_is_workbook_rule") and obj._is_workbook_rule:
            logging.debug(f"Found workbook rule in {file_path}: {obj.__name__}")
            rules.append(obj)
    return rules


def csv_data_rule(*args, **kwargs):
    applies_to = kwargs.get("applies_to", None)

    if len(args) == 1 and callable(args[0]):
        func = args[0]
        func._is_csv_data_rule = True
        func._applies_to = applies_to
        return func

    def decorator(func):
        func._is_csv_data_rule = True
        func._applies_to = applies_to
        return func

    return decorator


def workbook_rule(*args, **kwargs):
    if len(args) == 1 and callable(args[0]):
        func = args[0]
        func._is_workbook_rule = True
        return func

    def decorator(func):
        func._is_workbook_rule = True
        return func

    return decorator


def directory_to_module_path(directory_path):
    # Normalize the path to use the correct OS-specific separator
    normalized_path = os.path.normpath(directory_path)

    # Split the path into components
    path_components = normalized_path.split(os.sep)

    # Remove the file extension if present
    if path_components[-1].endswith(".py"):
        path_components[-1] = path_components[-1][:-3]

    # Join the components with dots to form the module path
    module_path = ".".join(path_components)

    return module_path


def validate_rules(rules, workbook):
    pass


def validate(args):
    if not args.rules:
        return

    modules = []
    for path in args.rules:
        if os.path.isdir(path):
            globbed = sorted(glob.glob(join(path, "*.py")))
            modules.extend(globbed)
        elif os.path.isfile(path):
            modules.append(path)
    modules = sorted(modules)
    logging.debug(f"Found modules: {modules}")

    rules = []
    # Validate CSV data rules.
    for module_path in modules:
        rules.extend(collect_csv_data_rules(module_path))
    for file_path in args.csv_files:
        for rule in rules:
            if rule._applies_to is None or basename(file_path) in rule._applies_to:
                with open(file_path, newline="") as f:
                    reader = csv.DictReader(f)
                    for row_num, row in enumerate(reader):
                        try:
                            errors = rule(file_path, row, row_num)
                        except RuleError as e:
                            logging.error(f"{file_path}: {e.message}")

    # Validate workbook rules.
    # Use openpyxl due to better support for reading data.
    wb = WorkbookFactory().with_config(args.config).build_openpyxl(args.csv_files)
    rules = []
    for module_path in modules:
        rules.extend(collect_workbook_rules(module_path))
    for rule in rules:
        try:
            errors = rule(wb)
        except RuleError as e:
            logging.error(e.message)

    #     v = getattr(rule, "validate")
    #     result = v(wb)
    #     if result:
    #         results.extend(result)
    # if results:
    #     for result in results:
    #         logging.error(f"{result.message}")
