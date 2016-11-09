from functools import partial
import datetime
from qubit.io.postgres import types
from qubit.io.postgres import QuerySet
from qubit.io.celery import queue
from qubit.io.celery import period_task
from qubit.io.celery import task_method
from qubit.types.function import Function
from qubit.types.qubit import Qubit

__all__ = ['Spout']


class Spout(Function):
    prototype = types.Table('spout', [
        ('name', types.varchar),
        ('body', types.text),
        ('closure', types.json),
        ('active', types.boolean),
        ('rate', types.integer)
    ])
    manager = QuerySet(prototype)

    @classmethod
    def activate_all(cls):
        list(map(cls.measure,
                 map(cls.format, cls.manager.filter(active=True))))

    @classmethod
    def measure(cls, spout):
        data = dict(datum=cls.activate(spout),
                    time=datetime.datetime.now())

        sig_name = '%s:%s' % (cls.__name__, spout.name)
        qubits = Qubit.get_flying(sig_name)
        for qubit in qubits:
            partial(Qubit.store_status,
                    data=data,
                    sender=None,
                    qid=qubit.id)()

    @staticmethod
    @partial(period_task, name='spout', period=1000)
    @queue.task(filter=task_method)
    def activate_period_task():
        return Spout.activate_all()
