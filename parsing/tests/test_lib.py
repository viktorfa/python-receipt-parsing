import unittest

from parsing.lib import get_ngrams, is_price, find_prices, find_weights, find_unit_prices, is_product
from receipt_scanning.Receipt import ReceiptLine

class TestBasic(unittest.TestCase):
  def test_get_ngrams(self):
    tokens = ['a', 'b', 'c', 'd']
    expected = [['a', 'b', 'c'], ['b', 'c', 'd']]
    n = 3
    actual = get_ngrams(tokens, n)
    self.assertListEqual(actual, expected)

  def test_is_price_gives_true_positive(self):
    token = '32,33'
    actual = is_price(token)
    self.assertTrue(actual)

  def test_is_price_gives_true_negative(self):
    token = '32,3'
    actual = is_price(token)
    self.assertFalse(actual)

  def test_find_prices(self):
    ngram = ['Herav', 'mom', '16,03']
    expected = [dict(
      value=16.03,
      index=2,
    )]
    actual = find_prices(ngram)
    print(actual)
    self.assertListEqual(actual, expected)

  def test_find_weights(self):
    ngram = ['0,088', 'kg', 'X']
    expected = [dict(
      value=0.088,
      index=0,
      unit='kg',
    )]
    actual = find_weights(ngram)
    self.assertListEqual(actual, expected)

  def test_find_unit_prices(self):
    ngram = ['kg', 'X', '29,90/kg']
    expected = [dict(
      value=29.90,
      index=2,
      unit='kg',
    )]
    actual = find_unit_prices(ngram)
    self.assertListEqual(actual, expected)

  def test_is_product_true_postive(self):
    ngram = ['1', 'Tine', 'melk', 'hel', '1T', '17,90']
    receipt_line = ReceiptLine(ngram)
    actual = is_product(receipt_line)
    self.assertTrue(actual)
    self.assertTrue(is_product(ReceiptLine(['Lok', '13,00'])))

  def test_is_product_true_negative(self):
    ngram = ['0,338', 'kg', 'X', '49,90/kg']
    receipt_line = ReceiptLine(ngram)
    actual = is_product(receipt_line)
    self.assertFalse(actual)
    self.assertFalse(is_product(ReceiptLine(['Org.nr.980', '371', '611', 'MVA'])))