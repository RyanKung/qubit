import time
from functools import wraps

__all__ = ['timer']


def timer(fn):
    @wraps(fn)
    def handler(*args, **kwargs):
        start = time.time()
        res = fn(*args, **kwargs)
        end = time.time()
        cost = str((end - start) * 1000.0)
        print('calling %s cost %s ms' % (fn.__name__, cost))
        return res
    return handler
