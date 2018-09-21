import unittest

from recread.parsing.tokens import get_product_name
from recread.receipt.models import ReceiptLine

class TestBasic(unittest.TestCase):
  def test_get_product_name(self):
    string_line = 'FRYDENLUNDPILSNER0,5L25%28,90'
    actual = get_product_name(string_line)
    expected = 'FRYDENLUNDPILSNER'
    self.assertEqual(actual, expected)

    string_line = '1Agurk14,90'
    actual = get_product_name(string_line)
    expected = 'Agurk'
    self.assertEqual(actual, expected)

  def test_get_product_name_edge_cases(self):
    string_line = ''
    actual = get_product_name(string_line)
    expected = ''
    self.assertEqual(actual, expected)

    string_line = None
    actual = get_product_name(string_line)
    expected = ''
    self.assertEqual(actual, expected)