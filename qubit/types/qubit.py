import json
from datetime import datetime
from qubit.io.postgres import types
from qubit.io.postgres import QuerySet
from qubit.types.function import Function

__all__ = ['Qubit', 'Status']


class Qubit(Function):

    prototype = types.Table('spout', [
        ('name', types.varchar),
        ('body', types.text),
        ('closure', types.json),
        ('active', types.boolean)
    ])
    manager = QuerySet(prototype)

    @classmethod
    def create(cls, name, body, closure={}, active=1):
        return cls.manager.insert(name=name,
                                  body=body,
                                  closure=json.dumps(closure),
                                  active=active)

    @classmethod
    def measure(cls):
        cls.manager.filter(active=True)
        pass

    @classmethod
    def entangle(cls, event):
        pass


class Status(object):
    prototype = types.Table('status', [
        ('spout', types.integer),
        ('name', types.varchar),
        ('datum', types.json),
        ('tags', types.text),
        ('timestamp', types.timestamp)
    ])

    manager = QuerySet(prototype)

    @classmethod
    def create(cls, spout, name, datum, timestamp=datetime.now(), tags=[]):
        return cls.manager.create(spout=spout,
                                  name=name,
                                  datum=datum,
                                  timestamp=timestamp,
                                  tags=tags)

    @classmethod
    def select(cls, sid, start, end):
        return cls.manager.find_in_range(spout=sid,
                                         start=start,
                                         end=end)
