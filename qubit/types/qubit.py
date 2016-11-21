import json
from functools import partial, reduce
from datetime import datetime
from qubit.io.postgres import types
from qubit.io.postgres import QuerySet
from qubit.io.celery import Entanglement
from qubit.io.celery import queue
from qubit.io.celery import task_method
from qubit.io.redis import client as kv
from qubit.types.utils import ts_data, empty_ts_data

__all__ = ['Qubit', 'States']


class QubitEntanglement(Entanglement):
    abstract = True

    def on_success(self, res, task_id, args, kwargs):
        pass


class Qubit(object):
    prototype = types.Table('qubit', [
        ('id', types.integer),
        ('name', types.varchar),
        ('entangle', types.varchar),
        ('body', types.varchar),
        ('flying', types.boolean)
    ])
    manager = QuerySet(prototype)

    @classmethod
    def create(cls, name, entangle, flying=True):
        qid = cls.manager.insert(name=name,
                                 entangle=entangle,
                                 flying=flying)
        return qid

    @classmethod
    def get(cls, qid):
        return cls.prototype(**cls.manager.get(qid))

    @classmethod
    def get_flying(cls, entangle):
        qubits = cls.manager.filter(entangle=entangle,
                                    flying=True)
        if not qubits:
            return []
        return list(map(lambda x: cls.prototype(**x), qubits))

    @classmethod
    def delete(cls, qubit_id):
        return cls.manager.delete(qubit_id)

    @classmethod
    def set_current(cls, qubit, ts_data):
        data = json.dumps(ts_data._asdict())
        key = 'qubit:%s:state' % qubit.id
        kv.set(key, data)
        return True

    @classmethod
    def get_current(cls, qubit):
        key = 'qubit:%s:state' % qubit.id
        data = kv.get(key)
        if not data:
            return empty_ts_data
        return ts_data(**json.loads(str(data)))

    @staticmethod
    @queue.task(filter=task_method, base=QubitEntanglement)
    def measure(qubit, data):    # S_q1(t1) = MR(S_q1(t0), S_q0(t1))
        if isinstance(qubit, dict):
            qubit = Qubit.prototype(**qubit)
        if isinstance(data, dict):
            data = ts_data(**data)
        datum = data.datum
        States.create(qubit=qubit.id,
                      datum=json.dumps(datum),
                      ts=data.ts,
                      tags=[])
        sig_name = '%s:%s' % ('Qubit', qubit.id)
        qubits = Qubit.get_flying(sig_name)
        if not qubits:
            return False
        qubits = map(lambda x: x._asdict(), qubits)
        list(map(partial(Qubit.measure.task.delay, data=data._asdict()), qubits))
        return True

    @classmethod
    def entangle(cls, qid1, qid2):
        sig_name = '%s:%s' % (cls.__name__, qid2)
        return cls.manager.update(qid1, entangle=sig_name)

    @classmethod
    def get_status(cls, qid):
        return States.get_by(qid)


class States(object):
    prototype = types.Table('states', [
        ('qubit', types.integer),
        ('datum', types.json),
        ('tags', types.text),
        ('ts', types.timestamp)
    ])

    manager = QuerySet(prototype)

    @classmethod
    def create(cls, qubit, datum, ts=datetime.now(), tags=[]):
        return dict(id=cls.manager.insert(qubit=qubit,
                                          datum=datum,
                                          ts=ts,
                                          tags=tags))

    @classmethod
    def format(cls, s: dict):
        return cls.prototype(
            qubit=s['qubit'],
            datum=s['datum'],
            tags=s.get('tags'),
            ts=s['ts'])

    @classmethod
    def select(cls, sid, start, end):
        res = cls.manager.find_in_range(qubit=sid,
                                        key='ts',
                                        start=start,
                                        end=end)
        return list(map(cls.format, res))

    @classmethod
    def get_via_qid(cls, qid):
        return cls.manager.get_by(qubit=qid)
