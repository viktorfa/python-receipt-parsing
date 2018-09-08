import unittest

from parsing.lib import get_ngrams, is_price, find_prices, find_weights, find_unit_prices

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