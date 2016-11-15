import json
from functools import lru_cache
from qubit.io.postgres import types
from qubit.io.postgres import QuerySet


__all__ = ['Function']


class Function(object):
    closure = types.Table('closure', [
        ('id', types.integer),
        ('closure', types.json)
    ])
    closure_manager = QuerySet(closure)

    @classmethod
    def create(cls, name, body, side_effect=False, closure=0, *args, **kwargs):
        if side_effect and not closure:
            closure = cls.closure_manager.insert(closure=json.dumps({}))
        if closure:
            closure = cls.closure_manager.insert(closure=json.dumps(closure))
        return cls.manager.insert(name=name,
                                  body=body,
                                  side_effect=side_effect,
                                  closure=closure,
                                  *args, **kwargs)

    @classmethod
    def get_closure(cls, ins):
        if ins.side_effect:
            return cls.closure_manager.get(ins.closure)['closure']
        else:
            return {}

    @classmethod
    def format(cls, raw: dict):
        if not raw:
            return None
        return cls.prototype(**raw)

    @classmethod
    def get_raw(cls, mid):
        return cls.format(cls.manager.get(mid))

    @classmethod
    def activate(cls, func):
        glo = dict(cls.get_closure(func),
                   **{'__import__': cls.__import__})
        return eval(func.body, glo)

    @classmethod
    def __import__(cls, s: str):
        if s or s not in ['os', 'sys']:
            return __import__(s)
        else:
            raise NotImplementedError

    @classmethod
    def get(cls, mid):
        return cls.activate(cls.get_raw(mid))

    @classmethod
    def get_list(cls, size=100, offset=0, sort_key=''):
        return cls.manager.get_list()

    @classmethod
    def delete(cls, mid):
        return cls.mapper.delete(id=mid)
