#! -*- eval: (venv-workon "qubit"); -*-

import json
import runpy
from types import ModuleType
from functools import partial
from qubit.io.pulsar import async
from qubit.io.postgres import types
from qubit.io.postgres import QuerySet
from qubit.io.celery import Entanglement
from qubit.io.celery import queue
from qubit.io.celery import task_method
from qubit.io.celery import period_task
from qubit.io.redis import client, cache, clear
from qubit.types.utils import ts_data, empty_ts_data
from qubit.types.states import States
from qubit.signals.signals import clear_flying_qubit_cache
__all__ = ['Qubit']


tell_client = partial(client.publish, 'eventsocket')


@clear_flying_qubit_cache.connect
def clear_flying_cache():
    clear('flying')


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
        clear('flying')
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
        whitelist = ['functools', 'operator',
                     'psutil',
                     'pandas', 'itertools']
        if name not in whitelist:
            return NotImplementedError
        return __import__(name, *args, **kwargs)

    @classmethod
    def send_data(cls, qid: str, data: str):
        assert isinstance(data, str)
        sck_name = 'qubitsocket::%s' % str(qid)
        client.publish(sck_name, json.dumps({'qid': qid, 'data': data}))

    @classmethod
    def update(cls, qid: str, data: dict):
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
        glo = {
            'datum': data.datum,
            '__builtins__': builtins
        }
        loc = {
            'qubit': qubit
        }
        Qubit.exec_monad(qubit.monad, glo, loc)
        datum = loc['datum']
        if not isinstance(datum, dict):
            datum = dict(raw=datum)
        return datum

    @staticmethod
    def exec_monad(monad: str, glo={}, loc={}):
        builtins = dict(__builtins__,
                        require=Qubit.require,
                        __import__=Qubit.__import__)
        glo = glo or {
            '__builtins__': builtins
        }
        exec(monad, glo, loc)

    @staticmethod
    @queue.task(filter=task_method, base=QubitEntanglement)
    @async
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
            cls.entanglement_trigger, cls.get_spouts()))

    @classmethod
    @cache(ttl=5000, flag='spout')
    def get_flying(cls, entangle):
        qubits = cls.manager.filter(
            entangle=entangle,
            flying=True)
        if not qubits:
            return []
        print(qubits)
        return list(map(lambda x: cls.prototype(**x)._asdict(), qubits))

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
        return (cls.manager.delete(qubit_id) and
                States.manager.delete_by(qubit=qubit_id))

    @classmethod
    def get_spem(cls, qid):
        '''
        Warning: A recursion calling
        '''
        qubit = cls.format_qubit(cls.get(qid))
        if qubit.is_stem:
            return qid
        kind, qid = qubit.entangle.split(':')
        if not kind == 'stem':
            return cls.get_spem(qid)
        else:
            return qid

    @classmethod
    def set_current(cls, qid, ts_data):
        data = json.dumps(ts_data._asdict())
        cls.send_data(qid, data)
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
        return (Qubit.format_qubit(qubit),
                Qubit.format_data(data))

    @staticmethod
    def format_qubit(qubit):
        if isinstance(qubit, dict):
            print(qubit)
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
    def entanglement_trigger(qubit, data={}):
        Qubit.activate.task.delay(
            qubit=qubit, data=data)

    @staticmethod
    def measure(qubit, depth):
        States.get_history(qubit.id, depth)

    @classmethod
    def trigger(cls, qubit, data):
        qubit, data = cls.format(qubit, data)
        name = qubit.is_stem and 'Stem' or 'Qubit'
        sig_name = '%s:%s' % (name, qubit.id)
        qubits = map(lambda x: cls.format_qubit(
            x)._asdict(), Qubit.get_flying(sig_name))
        if not qubits:
            return False
        res = list(map(partial(
            Qubit.entanglement_trigger,
            data=isinstance(data, dict) and data or data._asdict()), qubits))
        return res

    @classmethod
    def entangle(cls, qid1, qid2):
        sig_name = 'Qubit:%s' % qid2
        return cls.manager.update(qid1, entangle=sig_name)

    @staticmethod
    @partial(period_task, name='spout', period=300)
    @queue.task(filter=task_method)
    def activate_period_task():
        return Qubit.activate_all()

    @classmethod
    def pick_status(cls, qid, ts):
        return States.pick(qid, ts)
