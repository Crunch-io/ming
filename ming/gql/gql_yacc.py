from gql_lex import tokens

def p_statement(p):
    'statement : SELECT columns FROM ID where order limit'
    p[0] = ('select', p[2], p[4], p[5], p[6], p[7])

def p_columns_1(p):
    'columns : STAR'
    p[0] = ('*',)

def p_columns_2(p):
    'columns : columnlist'
    p[0] = p[1]

def p_columnlist_1(p):
    'columnlist : ID'
    p[0] = (p[1],)

def p_columnlist_2(p):
    'columnlist : columnlist COMMA ID'
    p[0] = p[1] + (p[3],)

def p_where_0(p):
    'where : empty'
    p[0] = ()

def p_where_1(p):
    'where : WHERE expr'
    p[0] = p[2]

def p_expr_1(p):
    '''expr : ID EQ rvalue
            | ID NE rvalue
            | ID LT rvalue
            | ID LE rvalue
            | ID GT rvalue
            | ID GE rvalue
            | ID IS rvalue
    '''
    p[0] = (p[2], p[1], p[3])

def p_expr_2(p):
    '''expr : expr AND expr'''
    p[0] = (p[2], p[1], p[3])

def p_rvalue_bind(p):
    '''rvalue : BIND_POS
              | BIND_NAME
    '''
    p[0] = ('bind', p[1])

def p_rvalue_literal(p):
    '''rvalue : TRUE
              | FALSE
              | NUMBER
              | STRING
    '''
    p[0] = p[1]

def p_order_by_0(p):
    '''order : empty'''
    p[0] = ()

def p_order_by_1(p):
    '''order : ORDER BY ID direction'''
    p[0] = (p[3], p[4])

def p_direction_0(p):
    '''direction : empty'''
    p[0] = 'ASC'

def p_direction_1(p):
    '''direction : ASC
                 | DESC
    '''
    p[0] = p[1]

def p_limit_0(p):
    '''limit : empty'''
    p[0] = ()

def p_limit_1(p):
    '''limit : LIMIT NUMBER'''
    p[0] = (p[1],)

def p_empty(p):
    'empty :'
    pass

# Error rule for syntax errors
def p_error(p):
    print "Syntax error in input!"
    import pdb; pdb.set_trace()
