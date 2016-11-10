import json
from functools import partial
from datetime import datetime
from blinker import signal
from qubit.io.postgres import types
from qubit.io.postgres import QuerySet

__all__ = ['Qubit', 'Status']


class Qubit(object):

    prototype = types.Table('qubit', [
        ('id', types.integer),
        ('name', types.varchar),
        ('entangle', types.varchar),
        ('mappers', types.array),
        ('reducer', types.integer),
        ('closure', types.json),
        ('flying', types.boolean)
    ])
    manager = QuerySet(prototype)

    @classmethod
    def create(cls, name, entangle, flying=True,
               reducer=0, mappers=[], closure={}):
        qid = cls.manager.insert(name=name,
                                 entangle=entangle,
                                 closure=json.dumps(closure),
                                 flying=flying,
                                 reducer=reducer,
                                 mappers=str(mappers).replace(
                                     '[', '{').replace(']', '}'))
        return qid

    @classmethod
    def get(cls, qid):
        return cls.prototype(**cls.manager.get(qid))

    @classmethod
    def measure(cls, qid):
        qubit = cls.get(qid)
        sig = signal(qubit.entangle)
        fn = partial(cls.store_status, qid=qid)
        sig.connect(fn)
        assert id(fn) in sig.receivers.keys()

    @classmethod
    def get_flying(cls, entangle):
        return list(map(lambda x: cls.prototype(**x), cls.manager.filter(
            entangle=entangle,
            flying=True)))

    @classmethod
    def store_status(cls, sender, data, qid, tags=[]):
        print('sotring')
        Status.create(qubit=qid,
                      datum=json.dumps(data.datum),
                      timestamp=data.ts,
                      tags=tags)

    @classmethod
    def entangle(cls, qid, event):
        cls.manager.update


class Status(object):
    prototype = types.Table('states', [
        ('qubit', types.integer),
        ('datum', types.json),
        ('tags', types.text),
        ('timestamp', types.timestamp)
    ])

    manager = QuerySet(prototype)

    @classmethod
    def create(cls, qubit, datum, timestamp=datetime.now(), tags=[]):
        return cls.manager.insert(qubit=qubit,
                                  datum=datum,
                                  timestamp=timestamp,
                                  tags=tags)

    @classmethod
    def select(cls, sid, start, end):
        return cls.manager.find_in_range(spout=sid,
                                         start=start,
                                         end=end)
