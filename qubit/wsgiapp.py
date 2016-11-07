from qubit.io.celery import queue
from qubit.io.celery import period_task
import qubit.types as types

__all__ = ['queue', 'types']


@queue.on_after_configure.connect
def setup_periodic_tasks(sender, **kwargs):
    return list(map(sender.add_periodic_task, period_task.tasks))
