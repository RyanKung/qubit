import json
from functools import partial
from datetime import datetime
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
        return dict(id=qid)

    @classmethod
    def get(cls, qid):
        return cls.prototype(**cls.manager.get(qid))

    @classmethod
    def get_flying(cls, entangle):
        return list(map(lambda x: cls.prototype(**x), cls.manager.filter(
            entangle=entangle,
            flying=True)))

    @classmethod
    def measure(cls, qubit, data):
        Status.create(qubit=qubit.id,
                      datum=json.dumps(data.datum),
                      timestamp=data.ts,
                      tags=[])
        sig_name = '%s:%s' % (cls.__name__, qubit.id)
        qubits = Qubit.get_flying(sig_name)
        list(map(partial(Qubit.measure, data=data), qubits))
        return True

    @classmethod
    def entangle(cls, qid1, qid2):
        sig_name = '%s:%s' % (cls.__name__, qid2)
        return cls.manager.update(qid1, entangle=sig_name)

    @classmethod
    def get_status(cls, qid):
        return Status.get_by(qid)


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
        return dict(id=cls.manager.insert(qubit=qubit,
                                          datum=datum,
                                          timestamp=timestamp,
                                          tags=tags))

    @classmethod
    def select(cls, sid, start, end):
        return cls.manager.find_in_range(qubit=sid,
                                         key='timestamp',
                                         start=start,
                                         end=end)

    @classmethod
    def get_via_qid(cls, qid):
        return cls.manager.get_by(qubit=qid)
