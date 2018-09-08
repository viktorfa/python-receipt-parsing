import re

price_pattern = r'\d+,\d{2}'
weight_pattern = r'\d+,\d{3}'
unit_price_pattern = r'\d+,\d{2}/kg'
product_text_pattern = r'[A-Za-z]+'
whole_word_price_pattern = r'^' + price_pattern + r'$'
whole_word_weight_pattern = r'^' + weight_pattern + r'$'
whole_word_unit_price_pattern = r'^' + unit_price_pattern + r'$'
group_price_pattern = r'(' + price_pattern + r')'
group_weight_pattern = r'(' + weight_pattern + r')'
group_unit_price_pattern = r'(' + unit_price_pattern + r')'



compiled_group_price_pattern = re.compile(group_price_pattern)
compiled_group_weight_pattern = re.compile(group_weight_pattern)
compiled_group_unit_price_pattern = re.compile(group_unit_price_pattern)

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
  return re.match(whole_word_price_pattern, token)

def find_prices(ngram):
  return [dict(value=parse_float(x), index=i) for i, x in enumerate(ngram) if is_price(x)]

def is_weight(token):
  return re.match(whole_word_weight_pattern, token)

def find_weights(ngram):
  return [dict(value=parse_float(x), index=i, unit=ngram[i+1] if i+1 < len(ngram) and ngram[i+1] in units else None) for i, x in enumerate(ngram) if is_weight(x)]

def is_unit_price(token):
  return re.match(whole_word_unit_price_pattern, token)

def find_unit_prices(ngram):
  return [dict(value=parse_float(x[:5]), index=i, unit=x[-2:]) for i, x in enumerate(ngram) if is_unit_price(x)]

def is_product(receipt_line):
  if len(receipt_line.prices) == 0:
    return False
  last_price = max(receipt_line.prices, key=lambda x: x['end_pos'])
  if not is_line_price(last_price, receipt_line):
    return False
  if not re.search(product_text_pattern, receipt_line.string_line):
    return False
  return True

def is_line_price(price, receipt_line):
  return price['end_pos'] == len(receipt_line.string_line)

def find_prices_in_string(string):
  matches = re.finditer(compiled_group_price_pattern, string)
  result = []
  for match in matches:
    start_pos, end_pos = match.regs[1]
    result.append(dict(value=parse_float(string[start_pos:end_pos]), start_pos=start_pos, end_pos=end_pos))
  return result
