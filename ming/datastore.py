from __future__ import with_statement
import time
import logging
from threading import Lock

from pymongo.connection import Connection
from pymongo.master_slave_connection import MasterSlaveConnection

from ming.utils import retry_on_autoreconnect
from . import mim

class AutoRetryConnection(Connection):
    '''Simple child class that retries (once) to send messages on
    AutoReconnect'''

    @retry_on_autoreconnect
    def _send_message(self, message, with_last_error=False):
        return super(AutoRetryConnection, self)._send_message(
            message, with_last_error=with_last_error)

    @retry_on_autoreconnect
    def _send_message_with_response(
        self, message, _must_use_master=False, **kwargs):
        return super(AutoRetryConnection, self)._send_message_with_response(
            message, _must_use_master=_must_use_master, **kwargs)

class Engine(object):
    '''Proxy for a pymongo connection, providing some url parsing'''

    def __init__(self, master='mongodb://localhost:27017/', slave=None,
                 connect_retry=3, use_gevent=False, use_auto_retry=False,
                 **connect_args):
        self._log = logging.getLogger(__name__)
        self._conn = None
        self._lock = Lock()
        self._connect_retry = connect_retry
        self._connect_args = connect_args
        if use_gevent:
            from . import async
            self.ConnectionClass = async.AsyncConnection
        elif use_auto_retry:
            self.ConnectionClass = AutoRetryConnection
        else:
            self.ConnectionClass = Connection
        self.configure(master, slave)

    def __repr__(self):
        return 'Engine(master=%r, slave=%r, **%r)' % (
            self.master_args,
            self.slave_args,
            self._connect_args)

    def configure(self, master='mongodb://localhost:27017/', slave=None):
        if master and master.startswith('mim://'):
            if slave:
                self._log.warning('Master/slave not supported with mim://')
                slave = None
            self._conn = mim.Connection.get()
        self.master_args = master
        self.slave_args = slave
        assert self.master_args or self.slave_args, \
            'You must specify either a master or a slave'
        if self.master_args and self.slave_args:
            hosts = self.slave_args[len('mongodb://'):]
            self._slave_hosts = ['mongodb://' + host for host in hosts.split(',') ]
        else:
            self._slave_hosts = []

    @property
    def conn(self):
        for attempt in xrange(self._connect_retry+1):
            if self._conn is not None: break
            with self._lock:
                if self._connect() is None:
                    time.sleep(1)
        return self._conn

    def _connect(self):
        self._conn = None
        master = None
        slaves = []
        try:
            if self.master_args:
                try:
                    master = self.ConnectionClass(self.master_args, **self._connect_args)
                except:
                    self._log.exception(
                        'Error connecting to master: %s', self.master_args)
            if self.slave_args and master:
                slaves = []
                for host in self._slave_hosts:
                    try:
                        slaves.append(self.ConnectionClass(
                                host, slave_okay=True, **self._connect_args))
                    except:
                        self._log.exception(
                            'Error connecting to slave: %s', host)
            if master:
                if slaves:
                    self._conn = MasterSlaveConnection(master, slaves)
                else:
                    self._conn = master
            elif self.slave_args:
                self._conn = self.ConnectionClass(self.slave_args, slave_okay=True, **self._connect_args)
        except:
            self._log.exception('Cannot connect to %s %s' % (self.master_args, self.slave_args))
        return self._conn

class DataStore(object):
    '''Engine bound to a particular database'''

    def __init__(self, master=None, slave=None, connect_retry=3,
                 bind=None, database=None, authenticate=None, **connect_args):
        '''
        :param master: connection URL(s) - mongodb://host:port[,host:port]
        :type master: string
        :param slave: like master, but slave(s)
        :type slave: string
        :param connect_retry: retry this many times (with 1-second sleep) when a Connection cannot be established
        :type connect_retry: int
        :param bind: instead of master and slave params, use an existing ming.datastore.Engine
        :param database: database name
        :param connect_args: arguments passed along to pymongo.Connect() such as network_timeout
        '''
        if bind is None:
            master=master or 'mongodb://localhost:27017/'
            bind = Engine(master, slave, connect_retry, **connect_args)
        self.bind = bind
        self.database = database
        self.authenticate = authenticate

    def __repr__(self):
        return 'DataStore(%r, %s)' % (self.bind, self.database)

    @property
    def conn(self):
        return self.bind.conn

    @property
    def db(self):
        db = getattr(self.bind.conn, self.database, None)
        if db and self.authenticate:
            db.authenticate(**self.authenticate)
        return db

class ShardedDataStore(object):
    _lock = Lock()
    _engines = {}

    @classmethod
    def get(cls, uri, database):
        with cls._lock:
            engine = cls._engines.get(uri)
            if not engine:
                engine = cls._engines[uri] = Engine(uri)
            return DataStore(bind=engine, database=database)
