import json
import runpy
from types import ModuleType
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


tell_client = partial(client.publish, 'eventsocket')


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
        ('store', types.boolean),
        ('comment', types.text),
        ('flying', types.boolean),
        ('rate', types.integer)
    ])
    manager = QuerySet(prototype)

    @classmethod
    def create(cls, name, entangle=None,
               flying=True, is_stem=False, is_spout=False,
               store=False, *args, **kwargs):
        qid = cls.manager.insert(
            name=name,
            entangle=entangle,
            is_stem=is_stem,
            is_spout=is_spout,
            store=store,
            flying=flying, *args, **kwargs)
        if qid and is_stem:
            tell_client('new_stem')
        return qid

    @staticmethod
    def require(name, *args, **kwargs):
        if '.py' not in name:
            name = name + '.py'
        module_dict = runpy.run_path(name)
        module = ModuleType(name)
        list(map(lambda x: setattr(module, *x), module_dict.items()))
        return module

    @staticmethod
    def __import__(name, *args, **kwargs):
        whitelist = ['functools', 'operator', 'pandas', 'itertools']
        if name not in whitelist:
            return NotImplementedError
        return __import__(name, *args, **kwargs)

    @classmethod
    def update(cls, qid, data):
        return cls.manager.update(qid, **data)

    @classmethod
    def get(cls, qid):
        return cls.prototype(**cls.manager.get(qid))

    @staticmethod
    def exec(qubit, data):
        qubit, data = Qubit.format(qubit, data)

        builtins = dict(__builtins__,
                        require=Qubit.require,
                        __import__=Qubit.__import__)
        glo = {'datum': data.datum, '__builtins__': builtins}
        loc = {}
        exec(qubit.monad, glo, loc)
        datum = loc['datum']
        if not isinstance(datum, dict):
            datum = dict(raw=datum)
        return datum

    @staticmethod
    @queue.task(filter=task_method,
                base=QubitEntanglement)
    def activate(qubit, data={}):
        qubit, data = Qubit.format(qubit, data)
        datum = Qubit.exec(qubit, data)
        data = ts_data(datum=datum, ts=data.ts)
        print(qubit._asdict())
        qubit.store and States.create(
            qubit=qubit.id,
            datum=json.dumps(datum),
            ts=data.ts,
            tags=[])
        Qubit.set_current(qubit.id, data)
        Qubit.trigger(qubit=qubit, data=data)

    @classmethod
    def activate_all(cls):
        return list(map(
            cls.measure, cls.get_spouts()))

    @classmethod
    @cache(ttl=5000, flag='spout')
    def get_flying(cls, entangle):
        qubits = cls.manager.filter(
            entangle=entangle,
            flying=True)
        if not qubits:
            return []
        return list(map(lambda x: cls.prototype(**x), qubits))

    @classmethod
    def get_spouts(cls):
        cached = client.get('qubit::spout_cache')
        return cached or list(map(
            cls.format_qubit,
            cls.manager.filter(flying=True, is_spout=True)))

    @classmethod
    def get_stem(cls):
        return list(map(
            cls.format_qubit,
            cls.manager.filter(flying=True, is_stem=True)))

    @classmethod
    def delete(cls, qubit_id):
        return cls.manager.delete(qubit_id) and States.manager.delete_by(qubit=qubit_id)

    @classmethod
    def get_spem(cls, qid):
        qubit = cls.format_qubit(cls.get(qid))
        kind, qid = qubit.entangle.split(':')
        if not kind == 'spem':
            return cls.get_Spem(qid)
        else:
            return qid

    @classmethod
    def set_current(cls, qid, ts_data):
        data = json.dumps(ts_data._asdict())
        tell_client('qubit::updated::%s::%s' % (qid, data))
        key = 'qubit:%s:state' % qid
        client.set(key, data)
        return True

    @classmethod
    def get_current(cls, qid):
        key = 'qubit:%s:state' % qid
        data = client.get(key)
        if not data:
            return empty_ts_data()
        return ts_data(**json.loads(data.decode()))

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
        if isinstance(qubit, list):
            qubit = Qubit.prototype(
                **dict(zip(Qubit.prototype._fields, qubit)))
        return qubit

    @staticmethod
    def format_data(data):
        if not data:
            return empty_ts_data()
        if isinstance(data, dict):
            data = ts_data(**data)
        if isinstance(data, list):
            data = ts_data(
                **dict(zip(ts_data._fields, data)))

        return data

    @staticmethod
    def measure(qubit, data={}):    # S_q1(t1) = MR(S_q1(t0), S_q0(t1))
        Qubit.activate.task.delay(
            qubit=qubit, data=data)

    @classmethod
    def trigger(cls, qubit, data):
        qubit, data = cls.format(qubit, data)
        name = qubit.is_stem and 'Stem' or 'Qubit'
        sig_name = '%s:%s' % (name, qubit.id)
        qubits = map(lambda x: cls.format_qubit(x)._asdict(), Qubit.get_flying(sig_name))
        if not qubits:
            return False
        res = list(map(partial(
            Qubit.measure,
            data=isinstance(data, dict) and data or data._asdict()), qubits))
        return res

    @classmethod
    def entangle(cls, qid1, qid2):
        sig_name = 'Qubit:%s' % qid2
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
    def select(cls, qid, start, end):
        res = cls.manager.find_in_range(
            qubit=qid, key='ts', start=start, end=end)
        return list(map(cls.format, res))

    @classmethod
    def pick(cls, sid, ts):
        return cls.manager.nearby(
            column='ts', value=ts, qubit=sid)[0]

    @classmethod
    def get_via_qid(cls, qid):
        return cls.manager.get_by(qubit=qid)
