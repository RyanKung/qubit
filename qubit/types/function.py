import json

__all__ = ['Function']


class Function(object):

    @classmethod
    def create(cls, name, body, closure={}, *args, **kwargs):
        return cls.manager.insert(name=name,
                                  body=body,
                                  closure=json.dumps(closure),
                                  *args, **kwargs)

    @classmethod
    def format(cls, raw: dict):
        return cls.prototype(**raw)

    @classmethod
    def get_raw(cls, mid):
        return cls.format(cls.manager.get(mid))

    @classmethod
    def activate(cls, func):
        return eval(func.body,
                    func.closure,
                    dict(__builtins__, __import__=cls.__import__))

    @staticmethod
    def __import__(cls, mod: str):
        '''
        like 'function'.'id'
        '''
        mod_path = mod.split('.')
        if (mod_path[0], mod_path[1]) == ('qubit', 'function'):
            return cls.activate(cls.get_raw(mod_path[-1]))
        else:
            return __import__(mod)

    @classmethod
    def delete(cls, mid):
        return cls.mapper.delete(id=mid)
