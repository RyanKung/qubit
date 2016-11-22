import json
from functools import partial
from datetime import datetime
from qubit.io.postgres import types
from qubit.io.postgres import QuerySet
from qubit.io.celery import Entanglement
from qubit.io.celery import queue
from qubit.io.celery import task_method
from qubit.io.celery import period_task
from qubit.io.redis import client, cache
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
        ('is_stem', types.boolean),
        ('is_spout', types.boolean),
        ('monad', types.text),
        ('flying', types.boolean),
        ('rate', types.integer)
    ])
    manager = QuerySet(prototype)

    @classmethod
    def create(cls, name, entangle=None,
               flying=True, *args, **kwargs):
        qid = cls.manager.insert(
            name=name,
            entangle=entangle,
            flying=flying, *args, **kwargs)
        return qid

    @classmethod
    def update(cls, name, data):
        return cls.manager.update_by(rule={'name': name}, **data)

    @classmethod
    def get(cls, qid):
        return cls.prototype(**cls.manager.get(qid))

    @staticmethod
    @queue.task(filter=task_method,
                base=QubitEntanglement)
    def activate(qubit, data={}):
        client.publish('eventsocket',
                       'qubit:active:%s' % qubit.name)
        return exec(qubit.monad, {
            '__import__': Qubit.__import__,
            'qubit': qubit,
            'data': data})
        Qubit.trigger(qubit=qubit, data=data)

    @classmethod
    def activate_all(cls):
        return list(map(
            cls.measure, cls.get_spouts()))

    @classmethod
    def get_flying(cls, entangle):
        qubits = cls.manager.filter(
            entangle=entangle,
            flying=True)
        if not qubits:
            return []
        return list(map(lambda x: cls.prototype(**x), qubits))

    @classmethod
    def get_spouts(cls):
        cached = client.get('qubit::all_flying_cache')
        client.publish('eventsocket', 'spout:checking')
        return cached or list(map(
            cls.format,
            cls.manager.filter(flying=True, is_spout=True)))

    @classmethod
    def delete(cls, qubit_id):
        return cls.manager.delete(qubit_id)

    @classmethod
    def set_current(cls, qubit, ts_data):
        data = json.dumps(ts_data._asdict())
        key = 'qubit:%s:state' % qubit.id
        client.set(key, data)
        return True

    @classmethod
    def get_current(cls, qubit):
        key = 'qubit:%s:state' % qubit.id
        data = client.get(key)
        if not data:
            return empty_ts_data
        return ts_data(**json.loads(str(data)))

    @classmethod
    def get_via_name(cls, name):
        return cls.forma_qubit(
            cls.get_by(name=name))

    @classmethod
    @cache(ttl=10000, flag='spout')
    def get_by(cls, name):
        return cls.manager.get_by(name=name)

    @staticmethod
    def format(qubit, data):
        return Qubit.format_qubit(qubit), Qubit.format_data(data)

    @staticmethod
    def format_qubit(qubit):
        if isinstance(qubit, dict):
            qubit = Qubit.prototype(**qubit)
        return qubit

    @staticmethod
    def format_data(data):
        if isinstance(data, dict):
            data = ts_data(**data)
        return data

    @staticmethod
    @queue.task(filter=task_method, base=QubitEntanglement)
    def measure(qubit, data):    # S_q1(t1) = MR(S_q1(t0), S_q0(t1))
        qubit, data = Qubit.format(qubit, data)
        datum = data.datum
        Qubit.activate.task.delay(
            qubit=qubit, data=data)
        States.create(qubit=qubit.id,
                      datum=json.dumps(datum),
                      ts=data.ts,
                      tags=[])

    @classmethod
    def trigger(cls, qubit, data):
        sig_name = '%s:%s' % ('Qubit', qubit.name)
        qubits = map(lambda x: x._asdict(), Qubit.get_flying(sig_name))
        if not qubits:
            return False
        res = list(map(partial(
            Qubit.measure.task.delay,
            data=isinstance(data, dict) and data or data._asdict()), qubits))
        return res

    @classmethod
    def entangle(cls, qid1, qid2):
        sig_name = '%s:%s' % (cls.__name__, qid2)
        return cls.manager.update(qid1, entangle=sig_name)

    @staticmethod
    @partial(period_task, name='spout', period=1000)
    @queue.task(filter=task_method)
    def activate_period_task():
        return Qubit.activate_all()

    @classmethod
    def pick_status(cls, qid, ts):
        return States.pick(qid, ts)


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
        return dict(id=cls.manager.insert(
            qubit=qubit, datum=datum,
            ts=ts, tags=tags))

    @classmethod
    def format(cls, s: dict):
        return cls.prototype(
            qubit=s['qubit'],
            datum=s['datum'],
            tags=s.get('tags'),
            ts=s['ts'])

    @classmethod
    def select(cls, sid, start, end):
        res = cls.manager.find_in_range(
            qubit=sid, key='ts', end=end)
        return list(map(cls.format, res))

    @classmethod
    def pick(cls, sid, ts):
        return cls.manager.nearby(
            column='ts', value=ts, qubit=sid)[0]

    @classmethod
    def get_via_qid(cls, qid):
        return cls.manager.get_by(qubit=qid)
