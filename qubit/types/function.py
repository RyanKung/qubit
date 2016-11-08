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
        raw.update({'closure': json.loads(raw['closure'])})
        return cls.prototype(**raw)

    @classmethod
    def get_raw(cls, mid):
        return cls.format(cls.manager.get(mid))

    @staticmethod
    def activate(func):
        return eval(func.body, func.closure)

    @classmethod
    def delete(cls, mid):
        return cls.mapper.delete(id=mid)
