'''
Test the gql layer
'''

from unittest import TestCase

import bson

from ming import mim
from ming.gql import gql_statement, gql_filter

class TestFilter(TestCase):

    def setUp(self):
        self.conn = mim.Connection()
        self.db = self.conn.test
        self.collection = self.db.foo

    def test_find_eq(self):
        doc = dict(a=5, b=6, _id=bson.ObjectId())
        self.collection.insert(doc)
        self.collection.insert({})
        result = list(gql_filter(self.collection, 'WHERE a=5'))
        self.assertEqual(result, [ doc ])

    def test_find_in(self):
        doc = dict(a=1, b=6, _id=bson.ObjectId())
        self.collection.insert(doc)
        self.collection.insert({})
        result = list(gql_filter(self.collection, 'WHERE a IN (1,2,3)'))
        self.assertEqual(result, [ doc ])

    def test_find_bind_pos(self):
        doc = dict(a=5, b=6, _id=bson.ObjectId())
        self.collection.insert(doc)
        self.collection.insert({})
        result = list(gql_filter(self.collection, 'WHERE a=:1', 5))
        self.assertEqual(result, [ doc ])

    def test_find_bind_name(self):
        doc = dict(a=5, b=6, _id=bson.ObjectId())
        self.collection.insert(doc)
        self.collection.insert({})
        result = list(gql_filter(self.collection, 'WHERE a=:bar', bar=5))
        self.assertEqual(result, [ doc ])

class TestStatement(TestCase):

    def setUp(self):
        self.conn = mim.Connection()
        self.db = self.conn.test
        self.collection = self.db.foo

    def test_find_eq(self):
        doc = dict(a=5, b=6, _id=bson.ObjectId())
        self.collection.insert(doc)
        self.collection.insert({})
        result = list(gql_statement(self.db, 'SELECT * FROM foo WHERE a=5'))
        self.assertEqual(result, [ doc ])

    def test_find_project(self):
        doc = dict(a=5, b=6, _id=bson.ObjectId())
        self.collection.insert(doc)
        self.collection.insert({})
        result = list(gql_statement(self.db, 'SELECT b FROM foo WHERE a=5'))
        self.assertEqual(result, [ dict(_id=doc['_id'], b=6) ])

    def test_find_key(self):
        doc = dict(a=5, b=6, _id=bson.ObjectId())
        self.collection.insert(doc)
        self.collection.insert({})
        result = list(gql_statement(self.db, 'SELECT __key__ FROM foo WHERE a=5'))
        self.assertEqual(result, [ dict(_id=doc['_id']) ] )

def test_parser():
    conn = mim.Connection()
    db = conn.test
    collection = db.foo
    args = (1,2,3)
    kwargs = dict(foo=4, bar=5)

    statements = (
        'SELECT a FROM b',
        'SELECT a,b FROM b',
        'SELECT * FROM b',
        'SELECT __key__ FROM b',
        'SELECT a FROM b WHERE c=1')
    filters = (
        'WHERE c=1',
        "WHERE c=1 AND d='1'",
        'WHERE c IN (1,2)',
        'WHERE c IN :1',
        'WHERE c IN :foo',
        'WHERE a = true',
        'WHERE a = false',
        'ORDER BY a',
        'ORDER BY a ASC',
        'ORDER BY a DESC',
        'ORDER BY a, b DESC',
        'LIMIT 4',
        'LIMIT 4,5',
        'OFFSET 2',
        'LIMIT 4 OFFSET 5',
        )
    for gql in statements:
        yield _check_statement, db, gql, args, kwargs
    for gql in filters:
        yield _check_filter, collection, gql, args, kwargs


def _check_statement(db, gql, args, kwargs):
    return gql_statement(db, gql, *args, **kwargs)

def _check_filter(collection, gql, args, kwargs):
    return gql_filter(collection, gql, *args, **kwargs)
