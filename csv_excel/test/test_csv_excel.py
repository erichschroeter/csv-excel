import tempfile
import unittest

from csv_excel.csv_excel import collect_worksheet_rules, column_to_index


class TestColumnToIndex(unittest.TestCase):
    def test_a_returns_0(self):
        self.assertEqual(column_to_index("A"), 0)

    def test_b_returns_1(self):
        self.assertEqual(column_to_index("B"), 1)


class TestCollectWorksheetRulesWithFiles(unittest.TestCase):
    def test_finds_one(self):
        with tempfile.TemporaryDirectory() as d:
            with tempfile.NamedTemporaryFile(dir=d, suffix=".py", delete=False) as f:
                f.write(
                    b"""
# We have to redefine in this temp file since importing the actual module is complicated.
def worksheet_rule(func):
    func.__annotations__['worksheet_rule'] = True
    return func

@worksheet_rule
def validate_something_a(reader):
    pass
                    """
                )
            collected = collect_worksheet_rules(f.name)
            self.assertEqual(1, len(collected))
            self.assertEqual("validate_something_a", collected[0].__name__)

    def test_finds_two(self):
        with tempfile.TemporaryDirectory() as d:
            with tempfile.NamedTemporaryFile(dir=d, suffix=".py", delete=False) as f:
                f.write(
                    b"""
# We have to redefine in this temp file since importing the actual module is complicated.
def worksheet_rule(func):
    func.__annotations__['worksheet_rule'] = True
    return func

@worksheet_rule
def validate_something_a(reader):
    pass

@worksheet_rule
def validate_something_b(reader):
    pass
                    """
                )
            collected = collect_worksheet_rules(f.name)
            self.assertEqual(2, len(collected))
