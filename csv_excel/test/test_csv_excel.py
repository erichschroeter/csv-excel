import unittest

from csv_excel.csv_excel import column_to_index


class TestColumnToIndex(unittest.TestCase):
    def test_a_returns_0(self):
        self.assertEqual(column_to_index('A'), 0)

    def test_b_returns_1(self):
        self.assertEqual(column_to_index('B'), 1)