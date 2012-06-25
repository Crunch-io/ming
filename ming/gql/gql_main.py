from ply import lex, yacc

import gql_lex, gql_yacc

lexer = lex.lex(module=gql_lex)

def gql_statement(database, gql, *args, **kwargs):
    parser = yacc.yacc(
        module=gql_yacc,
        start='statement',
        tabmodule='parsetab_gql_statement',
        debugfile='parser_gql_statement.out')
    parser.getbind = Binder(*args, **kwargs)
    result = parser.parse(gql, lexer=lexer)
    collection = database[result.pop('collection')]
    return collection.find(**result)

def gql_filter(collection, gql, *args, **kwargs):
    parser = yacc.yacc(
        module=gql_yacc,
        start='filter',
        tabmodule='parsetab_gql_filter',
        debugfile='parser_gql_filter.out')
    parser.getbind = Binder(*args, **kwargs)
    result = parser.parse(gql, lexer=lexer)
    return collection.find(**result)

class Binder(object):

    def __init__(self, *args, **kwargs):
        self.args = args
        self.kwargs = kwargs

    def __call__(self, name):
        try:
            return self.args[name-1]
        except (TypeError, IndexError):
            return self.kwargs[name]
