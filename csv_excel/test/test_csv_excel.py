import logging
import tempfile
import unittest

from csv_excel.csv_excel import (
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
