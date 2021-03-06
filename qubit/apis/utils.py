from concurrent.futures import TimeoutError
from pulsar import ensure_future
import simplejson as json
from functools import wraps

__all__ = ['jsonize', 'resp_wrapper']


def jsonize(fn):
    @wraps(fn)
    def handler(*args, **kwargs):
        data = fn(*args, **kwargs)
        return json.dumps(data, ensure_ascii=False,
                          ignore_nan=True, namedtuple_as_object=True,
                          default=str)
    return handler


def resp_wrapper(fn):
    @wraps(fn)
    def handler(*args, **kwargs):
        try:
            resp = fn(*args, **kwargs)
        except TimeoutError:
            resp = {}
        if not isinstance(resp, dict):
            resp = dict(data=resp)
        return dict(resp, result='ok', status_code='200')
    return handler
