import redis
import json
from functools import wraps
from pulsar.apps.data import create_store
from pulsar import ensure_future
from qubit.config import REDIS_PARMAS, REDIS_BACKEND

__all__ = ['kv_client', 'store', 'pubsub']

client = redis.StrictRedis(**REDIS_PARMAS)
store = create_store(REDIS_BACKEND)
pubsub = store.pubsub()


def cache(ttl=100, flag=None):
    def wrapper(fn):
        @wraps(fn)
        def handler(*args, **kwargs):
            key = "{fn_name}:{args}".format(**{
                'fn_name': flag or fn.__name__,
                'args': str(args)
            })
            cached_data = client.get(key)
            if cached_data:
                return json.loads(cached_data)
            else:
                res = fn(*args, **kwargs)
                client.set(key, json.dumps(res))
                client.expire(key, ttl)
                return res
        return handler
    return wrapper


def do_something(channel, message):
    return print(message, channel)

pubsub = store.pubsub()
pubsub.add_client(do_something)
ensure_future(pubsub.subscribe('mychannel', 'eventsocket'))
