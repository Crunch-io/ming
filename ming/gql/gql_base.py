class SyntaxError(Exception): pass

reserved = {
    'select': 'SELECT',
    'from': 'FROM',
    'where': 'WHERE',
    'order': 'ORDER',
    'by': 'BY',
    'desc': 'DESC',
    'asc': 'ASC',
    'and': 'AND',
    'or': 'OR',
    'is': 'IS',
    'in': 'IN',
    'limit': 'LIMIT',
    'offset': 'OFFSET',
    'true': 'TRUE',
    'false': 'FALSE',
    'ancestor': 'ANCESTOR' }

tokens = ['STAR', 'COMMA', 'ID', 'BIND_POS', 'BIND_NAME',
          'EQ', 'NE', 'LT', 'LE', 'GT', 'GE',
          'NUMBER', 'STRING', 'LPAREN', 'RPAREN'
          ]  + reserved.values()
