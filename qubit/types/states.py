from itertools import groupby
import datetime
from qubit.core.utils import tail
from qubit.measure import pandas
from qubit.io.postgres import types
from qubit.io.postgres import QuerySet

__all__ = ['States']


class States(object):
    prototype = types.Table('states', [
        ('qubit', types.integer),
        ('datum', types.json),
        ('tags', types.text),
        ('ts', types.timestamp)
    ])
    manager = QuerySet(prototype)

    @classmethod
    def create(cls, qubit: str, datum: dict,
               ts=datetime.datetime.now(), tags=[]):
        '''
        Create a new state data
        '''
        return dict(id=cls.manager.insert(
            qubit=qubit, datum=datum,
            ts=ts, tags=tags))

    @classmethod
    def format(cls, state_data: dict):
        '''
        map dict type dita to  self.prototype
        '''
        return cls.prototype(
            qubit=state_data['qubit'],
            datum=state_data['datum'],
            tags=state_data.get('tags'),
            ts=state_data['ts'])

    @classmethod
    def select(cls, qid, start, end=datetime.datetime.now(), lazy=False):
        '''
        query states via [start, end]
        '''
        res = cls.manager.find_in_range(
            qubit=qid, key='ts', start=start, end=end)
        return map(cls.format, res)

    @classmethod
    def select_lazy(cls, qid, start, end):
        '''
        query states via [start, end]
        '''
        return cls.manager.find_in_range_lazy(
            qubit=qid, key='ts', start=start, end=end)

    @classmethod
    def pick(cls, sid, ts):
        return cls.manager.nearby(
            column='ts', value=ts, qubit=sid)[0]

    @classmethod
    def get_via_qid(cls, qid):
        return cls.manager.get_by(qubit=qid)

    @classmethod
    def measure(cls, qid: str, sec: str) -> list:
        now = datetime.datetime.now()
        delta = datetime.timedelta(second=sec)
        return cls.manager.find_near_lazy(
            qubit=qid, key='ts', start=now - delta)

    @classmethod
    def get_period(cls, qid: str, period: str,
                   cycle: int, group_by=None) -> list:

        if int(cycle) > 12:  # refuse large data querying
            return []

        period_group_method = {
            'days': lambda d: d.day,
            'weeks': lambda d: d.isocalendar()[1],
            'months': lambda d: d.month,
            'years': lambda d: d.year
        }[period]

        period_delta = {
            'months': {'days': 30},
            'days': {'days': 1},
            'weeks': {'days': 1},
            'years': {'years': 1}
        }[period]

        def handler() -> [list]:
            now = datetime.datetime.now()
            delta_start = datetime.timedelta(**period_delta)
            start = now - delta_start
            grouped = groupby(cls.select(qid, start, now),
                              lambda x: getattr(
                                  x.ts, group_by or period_group_method))

            def calcu(data: dict) -> dict:
                ts = max(data.keys())
                df = pandas.DataFrame(data).T.describe()
                res = df.to_dict('index')
                return (ts, res)

            def map2df(g: groupby):  # itertools groupby
                return (calcu(dict(tuple(map(lambda x: (x.ts, x.datum), tail(g))))))

            return tuple(map(map2df, grouped))
        return handler()
