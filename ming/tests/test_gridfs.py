'''
Test the gridfs support
'''
import time

from unittest import TestCase
from collections import defaultdict

import mock

from ming import datastore
from ming import fs, Session

def mock_datastore():
    ds = mock.Mock()
    ds.db = defaultdict(mock_collection)
    return ds

def mock_collection():
    c = mock.Mock()
    c.find_one = mock.Mock(return_value={})
    return c

class TestFS(TestCase):

    def setUp(self):
        self.ds = datastore.DataStore('mim:///', database='test')
        self.Session = Session(bind=self.ds)
        self.TestFS = fs.filesystem(
            'test_fs', self.Session)

    def tearDown(self):
        self.ds.bind.conn.drop_all()

    def test_simple(self):
        with self.TestFS.m.new_file('test.txt') as fp:
            fp.write('The quick brown fox')
            fp.write(' jumped over the lazy dog')
        assert self.TestFS.m.exists(filename='test.txt')
        self.assertEqual(fp.filename, 'test.txt')
        self.assertEqual(fp.content_type, 'text/plain')
        fp = self.TestFS.m.get_last_version(filename='test.txt')
        self.assertEqual(
            fp.read(), 'The quick brown fox jumped over the lazy dog')
        self.assertEqual(self.TestFS.m.find().count(), 1)
        fobj = self.TestFS.m.get()
        self.assertEqual(fobj.filename, 'test.txt')
        self.assertEqual(fobj.content_type, 'text/plain')
        self.assertEqual(fobj.length, 44)
        fobj.m.delete()
        assert not self.TestFS.m.exists(filename='test.txt')
        fobj = self.TestFS.m.get()
        assert fobj is None

    def test_strange_mimetype(self):
        with self.TestFS.m.new_file('test.ming') as fp:
            fp.write('The quick brown fox')
            fp.write(' jumped over the lazy dog')
        self.assertEqual(fp.filename, 'test.ming')
        self.assertEqual(fp.content_type, 'application/octet-stream')

    def test_put(self):
        self.TestFS.m.put('test.txt', 'The quick brown fox')
        assert self.TestFS.m.exists(filename='test.txt')
        fp = self.TestFS.m.get_last_version(filename='test.txt')
        self.assertEqual(
            fp.read(), 'The quick brown fox')

    def test_get_file(self):
        self.TestFS.m.put('test.txt', 'The quick brown fox')
        fp = self.TestFS.m.get_last_version(filename='test.txt')
        fpid = fp._id
        self.assertEqual(self.TestFS.m.get_file(fpid).filename, 'test.txt')

    def test_get_version(self):
        self.TestFS.m.put('test.txt', 'The quick brown fox')
        time.sleep(0.01)
        self.TestFS.m.put('test.txt', 'jumped over the lazy dog')
        self.assertEqual(
            self.TestFS.m.get_last_version('test.txt').read(),
            'jumped over the lazy dog')
        self.assertEqual(
            self.TestFS.m.get_version('test.txt', 0).read(),
            'The quick brown fox')
        self.assertEqual(
            self.TestFS.m.get_version('test.txt', 1).read(),
            'jumped over the lazy dog')
        self.assertEqual(
            self.TestFS.m.get_version('test.txt', -1).read(),
            'jumped over the lazy dog')
        
        
