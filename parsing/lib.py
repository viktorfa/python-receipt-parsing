import re

price_pattern = r'^\d+,\d{2}$'
weight_pattern = r'^\d+,\d{3}$'
unit_price_pattern = r'^\d+,\d{2}/kg$'
compiled_price_pattern = re.compile(price_pattern)
compiled_weight_pattern = re.compile(weight_pattern)
compiled_unit_price_pattern = re.compile(unit_price_pattern)

units = [
  'kg',
  'g',
  'l',
  ]

def parse_float(string):
  try:
    return float(string.replace(',', '.'))
  except ValueError:
    return string

def get_ngrams(tokens, n):
  return [tokens[i:i+n] for i in range(len(tokens)-n+1)]

def is_price(token):
  return compiled_price_pattern.match(token)

def find_prices(ngram):
  return [dict(value=parse_float(x), index=i) for i, x in enumerate(ngram) if is_price(x)]

def is_weight(token):
  return compiled_weight_pattern.match(token)

def find_weights(ngram):
  return [dict(value=parse_float(x), index=i, unit=ngram[i+1] if i+1 < len(ngram) and ngram[i+1] in units else None) for i, x in enumerate(ngram) if is_weight(x)]

def is_unit_price(token):
  return compiled_unit_price_pattern.match(token)

def find_unit_prices(ngram):
  return [dict(value=parse_float(x[:5]), index=i, unit=x[-2:]) for i, x in enumerate(ngram) if is_unit_price(x)]