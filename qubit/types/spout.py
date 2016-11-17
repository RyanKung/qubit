from functools import partial
import datetime
import time
from qubit.io.postgres import types
from qubit.io.postgres import QuerySet
from qubit.io.celery import queue
from qubit.io.celery import period_task
from qubit.io.celery import task_method
from qubit.io.redis import kv_client as kv
from qubit.io.redis import cache
from qubit.types.qubit import Qubit
from qubit.types.utils import ts_data as ts_data

__all__ = ['Spout']


class Spout(object):
    prototype = types.Table('spout', [
        ('name', types.varchar),
        ('body', types.text),
        ('active', types.boolean),
        ('rate', types.integer),
        ('flying', types.boolean)
    ])
    manager = QuerySet(prototype)

    @classmethod
    def create(cls, name, body, flying=False, *args, **kwargs):
        flying and kv.delete('spout:all_flying_cache')  # clear cache
        return cls.manager.insert(name=name,
                                  body=body,
                                  flying=flying,
                                  *args, **kwargs)

    @classmethod
    def update(cls, name, data):
        return cls.manager.update_by(rule={'name': name}, **data)

    @classmethod
    def format(cls, raw: dict):
        if not raw:
            return None
        return cls.prototype(**raw)

    @classmethod
    def activate_all(cls):
        cached = kv.get('spout:all_flying_cache')
        return cached or list(map(cls.measure, cls.get_all_flying()))

    @classmethod
    def get_all_flying(cls):
        data = list(map(cls.format, cls.manager.filter(active=True, flying=True)))
        return data

    @classmethod
    def activate(cls, spout):
        return eval(spout.body, {'__import__': cls.__import__})

    @classmethod
    def __import__(cls, s: str):
        if s or s not in ['os', 'sys']:
            return __import__(s)
        else:
            raise NotImplementedError

    @classmethod
    def measure(cls, spout, data=None):  # S_q1(t1) = MR(S_q1(t0), S_q0(t1))
        if not data:
            ms = str(time.time()).split('.')[-1]
            if not(int(ms) % int(spout.rate)):
                return
            data = cls.get_status(spout)
        sig_name = '%s:%s' % (cls.__name__, spout.name)
        qubits = map(lambda x: x._asdict(), Qubit.get_flying(sig_name))
        res = list(map(partial(Qubit.measure.task.delay,
                               data=data._asdict()), qubits))
        return res

    @staticmethod
    @partial(period_task, name='spout', period=1)
    @queue.task(filter=task_method)
    def activate_period_task():
        return Spout.activate_all()

    @classmethod
    @cache(ttl=10000, flag='spout')
    def get_via_name(cls, name):
        return cls.format(cls.manager.get_by(name=name))

    @classmethod
    def get_status(cls, spout):
        data = ts_data(datum=cls.activate(spout),
                       ts=datetime.datetime.now())
        return data
