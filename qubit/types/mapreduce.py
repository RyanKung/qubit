from qubit.io.postgres import types
from qubit.io.postgres import QuerySet

__all__ = ['MapReducer']

mapper_table = types.Table('mapper', [
    ('name', types.varchar),
    ('side_effect', types.boolean),
    ('closure', types.json),
    ('body', types.json)
])

reducer_table = types.Table('mapper', [
    ('name', types.varchar),
    ('side_effect', types.boolean),
    ('closure', types.json),
    ('body', types.json)
])


def MapReducer(object):
    mapper = QuerySet(mapper_table)
    reducer = QuerySet(reducer_table)

    @classmethod
    def create_mapper(self, *args, **kwargs):
        return mapper.insert(*args, **kwargs)

    @classmethod
    def create_reducer(self, *args, **kwargs):
        return reducer.insert(*args, **kwargs)
