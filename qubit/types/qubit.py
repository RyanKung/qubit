import json
from functools import partial, reduce
from datetime import datetime
from qubit.io.postgres import types
from qubit.io.postgres import QuerySet
from qubit.io.celery import Entanglement
from qubit.io.celery import queue
from qubit.io.celery import task_method
from qubit.types.mapper import Mapper
from qubit.types.reducer import Reducer
from qubit.types.utils import ts_data

__all__ = ['Qubit', 'Status']


class QubitEntanglement(Entanglement):
    abstract = True

    def on_success(self, res, task_id, args, kwargs):
        pass


class Qubit(object):
    prototype = types.Table('qubit', [
        ('id', types.integer),
        ('name', types.varchar),
        ('entangle', types.varchar),
        ('mappers', types.array),
        ('reducer', types.integer),
        ('flying', types.boolean)
    ])
    manager = QuerySet(prototype)

    @classmethod
    def create(cls, name, entangle, flying=True,
               reducer=0, mappers=[]):
        qid = cls.manager.insert(name=name,
                                 entangle=entangle,
                                 flying=flying,
                                 reducer=reducer,
                                 mappers=str(mappers).replace(
                                     '[', '{').replace(']', '}'))
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
    def get_mappers(cls, qubit):
        if not qubit.mappers:
            return []
        return list(map(Mapper.get, qubit.mappers))

    @classmethod
    def add_mapper(cls, qubit_id, mapper_id):
        return cls.manager.append_array(qubit_id, key='mappers',
                                        value=mapper_id)

    @classmethod
    def get_reducer(cls, qubit):
        if not qubit.reducer:
            return None
        return Reducer.get(qubit.reducer)

    @classmethod
    def add_reducer(cls, qubit_id, reducer_id):
        return cls.manager.update(qubit_id, reducer=reducer_id)

    @classmethod
    def delete(cls, qubit_id):
        return cls.manager.delete(qubit_id)

    @classmethod
    def delete_mapper(cls, qubit_id, mapper_id):
        pass

    @classmethod
    def delete_reducer(cls, qubit_id, reducer_id):
        pass

    @classmethod
    def mapreduce(cls, qubit, data):
        mappers = cls.get_mappers(qubit)
        reducer = cls.get_reducer(qubit)
        datum = data.datum
        if mappers:
            datum = reduce(lambda x, y: y(x), mappers, datum)
        if reducer:
            datum = reduce(reducer, datum)
        return datum

    @staticmethod
    @queue.task(filter=task_method, base=QubitEntanglement)
    def measure(qubit, data):
        if isinstance(qubit, dict):
            qubit = Qubit.prototype(**qubit)
        if isinstance(data, dict):
            data = ts_data(**data)

        datum = Qubit.mapreduce(qubit, data)
        Status.create(qubit=qubit.id,
                      datum=json.dumps(datum),
                      timestamp=data.ts,
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
    def format(cls, s: dict):
        return cls.prototype(
            qubit=s['qubit'],
            datum=s['datum'],
            tags=s.get('tags'),
            timestamp=s['timestamp'])

    @classmethod
    def select(cls, sid, start, end):
        res = cls.manager.find_in_range(qubit=sid,
                                        key='timestamp',
                                        start=start,
                                        end=end)
        return list(map(cls.format, res))

    @classmethod
    def get_via_qid(cls, qid):
        return cls.manager.get_by(qubit=qid)
