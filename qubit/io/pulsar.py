from functools import partial
import pulsar

__all__ = ['period_task', 'async']


def period_task(fn):
    def task_wrapper(actor):
        return fn()
    if pulsar.get_actor():
        pulsar.spawn(period_task=task_wrapper)
    return fn


def async(fn):
    def task_wrapper(actor, *args, **kwargs):
        return fn(*args, **kwargs)
    fn.async = lambda *k, **kw: pulsar.spawn(start=partial(task_wrapper, *k, **kw))
    return fn
