from qubit.io.postgres import types
from qubit.io.postgres import QuerySet
from qubit.types.function import Function

__all__ = ['Reducer']


class Reducer(Function):
    prototype = types.Table('reducer', [
        ('name', types.varchar),
        ('side_effect', types.boolean),
        ('closure', types.json),
        ('body', types.text)
    ])
    manager = QuerySet(prototype)
