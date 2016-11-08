from functools import partial
from qubit.io.postgres import types
from qubit.io.postgres import QuerySet
from qubit.io.celery import queue
from qubit.io.celery import period_task
from qubit.io.celery import task_method
from qubit.types.function import Function

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
        return list(
            map(cls.activate,
                map(cls.format, cls.manager.filter(active=True))))

    @staticmethod
    @partial(period_task, name='spout', period=0.01)
    @queue.task(filter=task_method)
    def activate_period_task():
        return Spout.activate_all()
