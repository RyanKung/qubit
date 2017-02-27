import pandas
from functools import partial
import json
from types import GeneratorType

__all__ = ['pandas', 'LazyQueryReader']


class LazyQueryReader(object):
    def __init__(self, queryer: GeneratorType):
        self.g = queryer
        self.count = 0

    def read(self, n=0):
        try:
            query_res = list(next(self.g))
            if not query_res:
                return ''
            res = ','.join(list(map(
                partial(json.dumps, default=str),
                list(next(self.g))[0])))
            if res:
                self.count = self.count + 1
                return ('%s\n' % res).encode()
        except StopIteration:
            return ''

    def __iter__(self):
        return self

    def __next__(self):
        return self.read()


def read_generator(gen: GeneratorType, keys=[]):
    return pandas.read_csv(LazyQueryReader(gen),
                           lineterminator='\n',
                           names=list(keys),
                           engine='python')


pandas.read_gen = read_generator
