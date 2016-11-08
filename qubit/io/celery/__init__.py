import os
from typing import Callable
from celery import Celery
from celery import Task
from .types import PeriodTask

__all__ = ['queue', 'period_task']


class Entanglement(Task):
    abstract = True

os.environ['CELERY_CONFIG_MODULE'] = 'qubit.io.celery.config'
queue = Celery()


def period_task(fn: Callable, period=1, name='lambda'):
    if not period_task.__dict__.get('tasks'):
        period_task.__dict__['tasks'] = []
    period_task.__dict__['tasks'].append(
        PeriodTask(period, fn, name)
    )
    return fn


@queue.on_after_configure.connect
def setup_periodic_tasks(sender, **kwargs):
    for task in period_task.tasks:
        sender.add_periodic_task(task.period, task.task.s(), name=task.name)
