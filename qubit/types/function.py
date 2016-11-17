__all__ = ['Function']


class Function(object):
    @classmethod
    def create(cls, name, body, side_effect=False, *args, **kwargs):
        return cls.manager.insert(name=name,
                                  body=body,
                                  side_effect=side_effect,
                                  *args, **kwargs)

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
        glo = {'__import__': cls.__import__}
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
