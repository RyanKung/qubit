import redis
import simplejson as json
from functools import wraps
from pulsar.apps.data import create_store
from qubit.config import REDIS_PARMAS, REDIS_BACKEND

__all__ = ['client', 'store', 'pubsub',
           'clear']

client = redis.StrictRedis(**REDIS_PARMAS)
store = create_store(REDIS_BACKEND)
pubsub = store.pubsub()


def clear(flag=None):
    if not flag:
        flag = "*"
    else:
        flag += ':'
    keys = client.keys('qubit::%s' % flag)
    for k in keys:
        res = client.delete(k.decode())
        print('deleting %s %s' % (k.decode(), bool(res)))


def cache(ttl=100, flag=None):
    def wrapper(fn):
        @wraps(fn)
        def handler(*args, **kwargs):
            key = "qubit::{fn_name}:{args}".format(**{
                'fn_name': flag or fn.__name__,
                'args': str(args)
            })
            cached_data = client.get(key)
            if cached_data:
                return json.loads(cached_data.decode())['data']
            else:
                res = fn(*args, **kwargs)
                client.set(key, json.dumps(dict(data=res), namedtuple_as_object=True))
                client.expire(key, ttl)
                return res
        return handler
    return wrapper


pubsub = store.pubsub()
clear()
