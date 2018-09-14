import unittest

from recread.parsing.lib import get_ngrams, is_price, find_prices, find_weights, find_unit_prices,\
                        is_product, find_prices_in_string, is_line_price
from recread.receipt_scanning.Receipt import ReceiptLine

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
    
  def test_find_prices_in_string_true_positive(self):
    ngram = ['1', 'Tine', 'melk', 'hel', '1T', '17,90']
    string = ''.join(ngram)
    actual = find_prices_in_string(string)
    self.assertEqual(actual[0]['value'], 17.90)
    self.assertEqual(len(actual), 1)

    ngram = ['15', '%', '4', ',', '90', 'VANN', 'M', '/', 'KULLSYRE', 'F', '.', 'PRICE']
    string = ''.join(ngram)
    actual = find_prices_in_string(string)
    self.assertEqual(actual[0]['value'], 4.90)
    self.assertEqual(len(actual), 1)

  def test_find_prices_in_string_multiple_true_positive(self):
    ngram = ['25', ',', '00', '23', ',', '12', '90', '5', ',', '78']
    string = ''.join(ngram)
    actual = find_prices_in_string(string)
    self.assertEqual(len(actual), 3)

    ngram = ['15', '%', '4', ',', '90', 'VANN', 'M', '/', 'KULLSYRE', 'F', '.', 'PRICE']
    string = ''.join(ngram)
    actual = find_prices_in_string(string)
    self.assertEqual(actual[0]['value'], 4.90)
    self.assertEqual(len(actual), 1)


  def test_find_prices_in_string_true_negative(self):
    ngram = ['05', '/', '09', '/', '2018', '19', ':', '23']
    string = ''.join(ngram)
    actual = find_prices_in_string(string)
    self.assertEqual(len(actual), 0)

  def test_is_line_price_true_positive(self):
    ngram = ['FRYDENLUND', 'PILSNER', '0', ',', '5L', '25', '%', '28', ',', '90']
    receipt_line = ReceiptLine(ngram)
    price = receipt_line.prices[0]
    actual = is_line_price(price, receipt_line)
    self.assertTrue(actual)
    
    ngram = ['9', ',', '26', 'SUM', '53', ',', '34', '62', ',', '60']
    receipt_line = ReceiptLine(ngram)
    price = receipt_line.prices[-1]
    actual = is_line_price(price, receipt_line)
    self.assertTrue(actual)
