import logging
import tempfile
import unittest

from csv_excel.csv_excel import (
    collect_workbook_rules,
    column_to_index,
)


class TestColumnToIndex(unittest.TestCase):
    def test_a_returns_0(self):
        self.assertEqual(column_to_index("A"), 0)

    def test_b_returns_1(self):
        self.assertEqual(column_to_index("B"), 1)


class TestCollectWorksheetRulesWithFiles(unittest.TestCase):
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
        worksheet_annotation = """
def workbook_rule(*args, **kwargs):
    sheets = kwargs.get("sheets", None)

    if len(args) == 1 and callable(args[0]):
        func = args[0]
        func._is_workbook_rule = True
        func._sheets = sheets
        return func

    def decorator(func):
        func._is_workbook_rule = True
        func._sheets = sheets
        return func

    return decorator
"""
        content = worksheet_annotation + content
        logging.info(f"temp_file.name: {temp_file.name}")
        temp_file.write(content.encode())
        temp_file.close()
        return temp_file

    def test_finds_one_with_attributes(self):
        content = """
@workbook_rule(sheets=["A.csv", "B.csv"])
def validate_something_a(reader):
    pass
"""
        temp_file = self.create_temp_file_with_content(content)
        collected = collect_workbook_rules(temp_file.name)
        self.assertEqual(1, len(collected))
        self.assertEqual(["A.csv", "B.csv"], collected[0]._sheets)

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
