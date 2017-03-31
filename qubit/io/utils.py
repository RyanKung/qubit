import pulsar
import asyncio
from functools import wraps, partial
from typing import Callable
from types import coroutine
from threading import Thread
from multiprocessing import Process
from flask import request


__all__ = ['syncio', 'sync2async']

loop = pulsar.get_event_loop()


def syncio(fn, loop):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        return loop.run_until_complete(fn(*args, **kwargs))
    return wrapper


def sync2async(fn: Callable) -> coroutine:
    async def handler(*args, **kwargs):
        def wrapper(ft: asyncio.Future):
            print('call wrapper')
            res = fn(*args, **kwargs)
            ft.set_result(res)
            loop.stop()
        future = asyncio.Future()
        loop.call_later(0, partial(wrapper, future))
        return future
    return handler


def with_new_thread(fn):
    def _(*args, **kwargs):
        def _(loop):
            asyncio.set_event_loop(loop)
            loop.run_forever()
        loop = asyncio.new_event_loop()
        Thread(target=_, args=(loop,)).start()
        feature = asyncio.run_coroutine_threadsafe(fn(*args, **kwargs), loop)
        return feature.result()
    return _


def with_loop(fn):
    def _(*args, **kwargs):
        try:
            loop = request.environ.get('pulsar.connection')._loop
            return loop.run_until_complete(fn(*args, **kwargs))
        except OSError:
            print('gen new loop !!!!!!!', OSError)
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            res = loop.run_until_complete(fn(*args, **kwargs))
            return res
        except RuntimeError as ex:
            # if ex.args[0] == 'Event loop is running.':
            #     res = with_new_thread(fn)(*args, **kwargs)
            #     return res
            # if ex.args[0] == 'Event loop is closed':
            #     res = with_new_thread(fn)(*args, **kwargs)
            #     return res
            raise ex
    return _
