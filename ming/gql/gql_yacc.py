from gql_lex import tokens

BSON_OPERATORS = {
    '=': '$eq',
    '!=': '$ne',
    '<': '$lt',
    '<=': '$le',
    '>': '$gt',
    '>=': '$ge',
    'IS': '$eq' }

def p_statement(p):
    'statement : SELECT columns FROM ID filter'
    p[0] = dict(
        collection=p[4],
        fields=p[2])
    p[0].update(p[5])

def p_filter(p):
    'filter : where order limit offset'
    p[0] = dict()
    p[0].update(p[1])
    p[0].update(p[2])
    p[0].update(p[3])
    p[0].update(p[4])

def p_columns_1(p):
    'columns : STAR'
    p[0] = None

def p_columns_2(p):
    'columns : columnlist'
    p[0] = p[1]

def p_columnlist_1(p):
    'columnlist : ID'
    p[0] = { p[1]: 1 }

def p_columnlist_2(p):
    'columnlist : columnlist COMMA ID'
    p[0] = dict(p[1])
    p[0][p[3]] = 1

def p_where_0(p):
    'where : empty'
    p[0] = dict(spec={})

def p_where_1(p):
    'where : WHERE expr'
    p[0] = dict(spec=p[2])

def p_expr_1(p):
    '''expr : ID EQ rvalue
            | ID NE rvalue
            | ID LT rvalue
            | ID LE rvalue
            | ID GT rvalue
            | ID GE rvalue
            | ID IS rvalue
    '''
    operator = BSON_OPERATORS[p[2]]
    p[0] = { p[1]: { operator: p[3] } }

def p_expr_1a(p):
    '''expr : ID IN LPAREN literal_list RPAREN'''
    p[0] = { p[1]: { '$in': p[4] } }

def p_expr_1b(p):
    '''expr : ID IN bindval'''
    p[0] = { p[1]: { '$in': p[3] } }

def p_expr_2(p):
    '''expr : expr AND expr'''
    p[0] = dict(p[1])
    p[0].update(p[3])

def p_rvalue(p):
    '''rvalue : literal
              | bindval'''
    p[0] = p[1]

def p_bindval(p):
    '''bindval : BIND_POS
              | BIND_NAME
    '''
    p[0] = p.parser.getbind(p[1])

def p_literal_list_0(p):
    '''literal_list : literal'''
    p[0] = [ p[1] ]

def p_literal_list_1(p):
    '''literal_list : literal_list COMMA literal'''
    p[0] = p[1]
    p[0].append(p[3])

def p_literal_bool(p):
    '''literal : TRUE
               | FALSE
    '''
    if p[1].lower() == 'true':
        p[0] = True
    elif p[1].lower() == 'false':
        p[0] = False
    else: # pragma no cover
        raise ValueError, '%s is neither "true" nor "false"' % (
            p[1])

def p_literal_other(p):
    '''literal : NUMBER
               | STRING
    '''
    p[0] = p[1]

def p_order_by_0(p):
    '''order : empty'''
    p[0] = dict(sort=None)

def p_order_by_1(p):
    '''order : ORDER BY order_by_list'''
    p[0] = dict(sort=p[3])

def p_order_by_list_0(p):
    '''order_by_list : ID direction'''
    p[0] = [ (p[1], p[2]) ]

def p_order_by_list_1(p):
    '''order_by_list : order_by_list COMMA ID direction'''
    p[0] = p[1] + [ (p[3], p[4]) ]

def p_direction_0(p):
    '''direction : empty'''
    p[0] = 1

def p_direction_1(p):
    '''direction : ASC
                 | DESC
    '''
    if p[1].lower() == 'asc':
        p[0] = 1
    else:
        p[0] = -1

def p_limit_0(p):
    '''limit : empty'''
    p[0] = dict(limit=None)

def p_limit_1(p):
    '''limit : LIMIT NUMBER'''
    p[0] = dict(limit=p[2])

def p_limit_2(p):
    '''limit : LIMIT NUMBER COMMA NUMBER'''
    p[0] = dict(skip=p[2], limit=p[4])

def p_offset_0(p):
    '''offset : empty'''
    p[0] = dict(skip=None)

def p_offset_1(p):
    '''offset : OFFSET NUMBER'''
    p[0] = dict(skip=p[2])

def p_empty(p):
    'empty :'
    pass

# Error rule for syntax errors
def p_error(p): # pragma no cover
    print "Syntax error in input!"
    import pdb; pdb.set_trace()

