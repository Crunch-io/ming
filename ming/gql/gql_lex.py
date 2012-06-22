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
    'limit': 'LIMIT',
    'true': 'TRUE',
    'false': 'FALSE' }

tokens = ['STAR', 'COMMA', 'ID', 'BIND_POS', 'BIND_NAME',
          'EQ', 'NE', 'LT', 'LE', 'GT', 'GE',
          'NUMBER', 'STRING'
          ]  + reserved.values()

t_STAR = r'\*'
t_COMMA = r','
t_EQ = r'='
t_NE = r'!='
t_LT = r'<'
t_LE = r'<='
t_GT = r'>'
t_GE = r'>='

t_ignore = ' \t'

def t_BIND_POS(t):
    r':\d+'
    t.value = int(t.value[1:])
    return t

def t_BIND_NAME(t):
    r':[a-zA-Z_][a-zA-Z_0-9]*'
    return t

def t_NUMBER(t):
    r'\d+'
    t.value = int(t.value)
    return t

def t_STRING(t):
    r"""\'(\\.|[^"])*\'"""
    t.value = t.value[1:-1]
    return t

def t_ID(t):
    r'[a-zA-Z_][a-zA-Z_0-9]*'
    t.type = reserved.get(t.value.lower(),'ID')    # Check for reserved words
    return t

def t_error(t):
    print 'Illegal character "%s"' % t.value[0]
    t.lexer.skip(1)
