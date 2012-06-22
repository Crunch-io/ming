import sys
from ply import lex, yacc

import gql_lex, gql_yacc

def main():
    lexer = lex.lex(module=gql_lex)
    filter_parser = yacc.yacc(
        module=gql_yacc,
        start='filter',
        tabmodule='parsetab_gql_filter',
        debugfile='parser_gql_filter.out')
    filter_parser.getbind = lambda name: '$' + repr(name)
    for f in filters:
        print 'Parse %r' % f
        result = filter_parser.parse(f, lexer=lexer)
        print '''find(
            %(spec)r,
            limit=%(limit)r,
            sort=%(sort)r''' % result

    statement_parser = yacc.yacc(
        module=gql_yacc,
        start='statement',
        tabmodule='parsetab_gql_statement',
        debugfile='parser_gql_statement.out')
    statement_parser.getbind = lambda name: '$' + repr(name)
    for stmt in statements:
        print 'Parse %r' % stmt
        result = statement_parser.parse(stmt, lexer=lexer)
        print '''db.%(collection)s.find(
            %(spec)r,
            fields=%(fields)r,
            limit=%(limit)r,
            sort=%(sort)r''' % result

def test_generator():
    for f in filters:
        stmt = 'SELECT a,b,c FROM table ' + f
        yield stmt
    for stmt in statements:
        yield stmt


filters = [
    'WHERE patch = :1 AND left = FALSE ORDER BY date',
    'WHERE patch = :1 ORDER BY date',
    'WHERE closed = FALSE AND private = FALSE'
    '    ORDER BY modified DESC',
    'WHERE a = :1 AND private = FALSE'
    '    ORDER BY modified DESC',
    'WHERE ANCESTOR IS :1 AND draft = FALSE',
    'WHERE ANCESTOR IS :1 AND author = :2 AND draft = TRUE',
    'WHERE patch = :1 AND draft = FALSE',
    'WHERE patch = :1 AND draft = TRUE AND author = :2',
    'WHERE lower_nickname >= :1 AND lower_nickname < :2',
    'WHERE author = :1 AND draft = TRUE',
    'WHERE lower_nickname = :1',
    'WHERE patchset = :1 AND filename = :2',
    'WHERE ANCESTOR IS :1 AND draft = TRUE'
    '  AND author = :2',
    'WHERE ANCESTOR IS :1 AND draft = FALSE',
    'WHERE ANCESTOR IS :1',
    'WHERE ANCESTOR IS :1',
    'WHERE ANCESTOR IS :1',
    "WHERE patchset = :1",
    'WHERE patchset = :1 AND filename = :2',
    'WHERE patchset = :1 AND filename = :2',
    "WHERE patchset = :1 ORDER BY filename",
    "WHERE patchset = :1 ORDER BY filename",
    'WHERE patch = :patch AND lineno = :lineno AND left = :left '
    '    ORDER BY date',
    'WHERE issue = :1 AND sender = :2 '
    '    AND draft = TRUE',
    'WHERE ANCESTOR IS :1 AND author = :2 AND draft = TRUE',
    'WHERE issue = :1 AND sender = :2'
    '    AND draft = TRUE',
    'WHERE owner = :1',
    "WHERE name = 'Python'",
    'WHERE repo = :1',
    'WHERE repo = :1'
    ]
statements = [
    'SELECT * FROM Issue'
    '    WHERE private = FALSE'
    '    ORDER BY modified DESC',
    'SELECT * FROM Issue'
    '    WHERE closed = FALSE AND private = FALSE '
    '    ORDER BY modified DESC',
    'SELECT * FROM Issue '
    '    WHERE closed = FALSE AND owner = :1 '
    '    ORDER BY modified DESC '
    '    LIMIT 100',
    'SELECT * FROM Issue '
    '    WHERE closed = FALSE AND reviewers = :1 '
    '    ORDER BY modified DESC '
    '    LIMIT 100',
    'SELECT * FROM Issue '
    '    WHERE closed = TRUE AND modified > :1 AND owner = :2 '
    '    ORDER BY modified DESC '
    '    LIMIT 100',
    'SELECT * FROM Issue '
    '    WHERE closed = FALSE AND cc = :1 '
    '    ORDER BY modified DESC '
    '    LIMIT 100',
    'SELECT * FROM Message WHERE ANCESTOR IS :1 AND sender = :2',
    'SELECT * FROM Issue'
    '    WHERE closed = FALSE AND owner = :1',
    'SELECT * FROM Issue'
    '    WHERE closed = FALSE AND reviewers = :1',
    ]

def pm(etype, value, tb): # pragma no cover
    import pdb, traceback
    try:
        from IPython.ipapi import make_session; make_session()
        from IPython.Debugger import Pdb
        sys.stderr.write('Entering post-mortem IPDB shell\n')
        p = Pdb(color_scheme='Linux')
        p.reset()
        p.setup(None, tb)
        p.print_stack_trace()
        sys.stderr.write('%s: %s\n' % ( etype, value))
        p.cmdloop()
        p.forget()
        # p.interaction(None, tb)
    except ImportError:
        sys.stderr.write('Entering post-mortem PDB shell\n')
        traceback.print_exception(etype, value, tb)
        pdb.post_mortem(tb)

sys.excepthook = pm

if __name__ == '__main__':
    main()
