import redis
import json
from functools import wraps
from qubit.config import REDIS_PARMAS

__all__ = ['kv_client']

kv_client = redis.StrictRedis(**REDIS_PARMAS)


def cache(ttl=100, flag=None):
    def wrapper(fn):
        @wraps(fn)
        def handler(*args, **kwargs):
            key = "{fn_name}:{args}".format(**{
                'fn_name': flag or fn.__name__,
                'args': str(args)
            })
            cached_data = kv_client.get(key)
            if cached_data:
                return json.loads(cached_data)
            else:
                res = fn(*args, **kwargs)
                kv_client.set(key, json.dumps(res))
                kv_client.expire(key, ttl)
                return res
        return handler
    return wrapper
