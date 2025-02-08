import logging
import os
import tempfile
import unittest

from csv_excel.csv_excel import (
    ExcelWorkbook,
    OpenPyxlStrategy,
    XlsxWriterStrategy,
    collect_csv_data_rules,
    collect_workbook_rules,
    column_to_index,
)


class TestColumnToIndex(unittest.TestCase):
    def test_a_returns_0(self):
        self.assertEqual(column_to_index("A"), 0)

    def test_b_returns_1(self):
        self.assertEqual(column_to_index("B"), 1)


class TestCollectCsvDataRulesWithFiles(unittest.TestCase):
    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        return super().setUp()

    def tearDown(self):
        self.temp_dir.cleanup()

    def create_temp_file_with_content(self, content):
        temp_file = tempfile.NamedTemporaryFile(
            dir=self.temp_dir.name, suffix=".py", delete=False
        )
        # We have to redefine in the decorator since importing the actual module unit tests is complicated.
        annotation = """
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
"""
        content = annotation + content
        logging.info(f"temp_file.name: {temp_file.name}")
        temp_file.write(content.encode())
        temp_file.close()
        return temp_file

    def test_finds_one_with_attributes(self):
        content = """
@csv_data_rule(applies_to=["A.csv", "B.csv"])
def validate_something_a(reader):
    pass
"""
        temp_file = self.create_temp_file_with_content(content)
        collected = collect_csv_data_rules(temp_file.name)
        self.assertEqual(1, len(collected))
        self.assertEqual(["A.csv", "B.csv"], collected[0]._applies_to)

    def test_finds_one(self):
        content = """
@csv_data_rule
def validate_something_a(reader):
    pass
"""
        temp_file = self.create_temp_file_with_content(content)
        collected = collect_csv_data_rules(temp_file.name)
        self.assertEqual(1, len(collected))
        self.assertEqual("validate_something_a", collected[0].__name__)

    def test_finds_two(self):
        content = """
@csv_data_rule
def validate_something_a(reader):
    pass

@csv_data_rule
def validate_something_b(reader):
    pass
"""
        temp_file = self.create_temp_file_with_content(content)
        collected = collect_csv_data_rules(temp_file.name)
        self.assertEqual(2, len(collected))


class TestCollectWorkbookRulesWithFiles(unittest.TestCase):
    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        return super().setUp()

    def tearDown(self):
        self.temp_dir.cleanup()

    def create_temp_file_with_content(self, content):
        temp_file = tempfile.NamedTemporaryFile(
            dir=self.temp_dir.name, suffix=".py", delete=False
        )
        # We have to redefine in the decorator since importing the actual module unit tests is complicated.
        annotation = """
def workbook_rule(*args, **kwargs):
    if len(args) == 1 and callable(args[0]):
        func = args[0]
        func._is_workbook_rule = True
        return func

    def decorator(func):
        func._is_workbook_rule = True
        return func

    return decorator
"""
        content = annotation + content
        logging.info(f"temp_file.name: {temp_file.name}")
        temp_file.write(content.encode())
        temp_file.close()
        return temp_file

    def test_finds_one(self):
        content = """
@workbook_rule
def validate_something_a(reader):
    pass
"""
        temp_file = self.create_temp_file_with_content(content)
        collected = collect_workbook_rules(temp_file.name)
        self.assertEqual(1, len(collected))
        self.assertEqual("validate_something_a", collected[0].__name__)

    def test_finds_two(self):
        content = """
@workbook_rule
def validate_something_a(reader):
    pass

@workbook_rule
def validate_something_b(reader):
    pass
"""
        temp_file = self.create_temp_file_with_content(content)
        collected = collect_workbook_rules(temp_file.name)
        self.assertEqual(2, len(collected))


class TestValidateCsvDataRules(unittest.TestCase):
    def setUp(self):
        pass

    def test_(self):
        pass


class TestValidateWorkbookRules(unittest.TestCase):
    def setUp(self):
        self.strategy = XlsxWriterStrategy()
        self.wb = ExcelWorkbook(self.strategy)

    def test_add_worksheet(self):
        self.wb.add_worksheet("Sheet1")
        self.assertEqual("Sheet1", self.wb.workbook.worksheets()[0].name)

    # def test_create_format(self):
    #     self.wb.create_format({"bold": True})
    #     self.assertEqual(xlsxwriter.Format(), self.wb.workbook.worksheets()[0].name)


class TestExcelWorkbook(unittest.TestCase):
    def setUp(self):
        self.xlsxwriter_strategy = XlsxWriterStrategy()
        self.openpyxl_strategy = OpenPyxlStrategy()

    def test_add_worksheet_xlsxwriter(self):
        workbook = ExcelWorkbook(self.xlsxwriter_strategy)
        worksheet = workbook.add_worksheet("Sheet1")
        self.assertIsNotNone(worksheet)
        self.assertIn("Sheet1", workbook.worksheets)

    def test_add_worksheet_openpyxl(self):
        workbook = ExcelWorkbook(self.openpyxl_strategy)
        worksheet = workbook.add_worksheet("Sheet1")
        self.assertIsNotNone(worksheet)
        self.assertIn("Sheet1", workbook.worksheets)

    def test_write_data_xlsxwriter(self):
        workbook = ExcelWorkbook(self.xlsxwriter_strategy)
        workbook.add_worksheet("Sheet1")
        workbook.write_data("Sheet1", 0, 0, "Hello")
        # Since xlsxwriter doesn't allow reading back data, we just ensure no exceptions are raised

    def test_write_data_openpyxl(self):
        workbook = ExcelWorkbook(self.openpyxl_strategy)
        workbook.add_worksheet("Sheet1")
        workbook.write_data("Sheet1", 0, 0, "Hello")
        self.assertEqual(
            workbook.worksheets["Sheet1"].cell(row=1, column=1).value, "Hello"
        )

    def test_create_format_xlsxwriter(self):
        workbook = ExcelWorkbook(self.xlsxwriter_strategy)
        cell_format = workbook.create_format(font_color="red", bg_color="yellow")
        self.assertIsNotNone(cell_format)

    def test_create_format_openpyxl(self):
        workbook = ExcelWorkbook(self.openpyxl_strategy)
        cell_format = workbook.create_format(font_color="FF0000", bg_color="FFFF00")
        self.assertIsNotNone(cell_format)
        self.assertIn("font", cell_format)
        self.assertIn("fill", cell_format)

    def test_save_xlsxwriter(self):
        workbook = ExcelWorkbook(self.xlsxwriter_strategy)
        workbook.add_worksheet("Sheet1")
        with tempfile.NamedTemporaryFile(delete=False, suffix=".xlsx") as tmp:
            workbook.save(tmp.name)
            self.assertTrue(os.path.exists(tmp.name))
            os.remove(tmp.name)

    def test_save_openpyxl(self):
        workbook = ExcelWorkbook(self.openpyxl_strategy)
        workbook.add_worksheet("Sheet1")
        with tempfile.NamedTemporaryFile(delete=False, suffix=".xlsx") as tmp:
            workbook.save(tmp.name)
            self.assertTrue(os.path.exists(tmp.name))
            os.remove(tmp.name)
