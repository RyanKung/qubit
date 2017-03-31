#! -*- eval: (venv-workon "qubit"); -*-

from itertools import groupby, starmap
import datetime
from dateutil.relativedelta import relativedelta
from qubit.core.utils import tail
from qubit.measure import pandas
from qubit.io.postgres import types
from qubit.io.postgres import QuerySet
from qubit.io.redis import cache
from qubit.types.utils import DateRange

__all__ = ['States']

METRIC = ('years', 'months', 'weeks', 'days', 'hours', 'minutes', 'seconds')


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

    @staticmethod
    def shift(t: datetime.datetime, k: str, v: int):
        return t - relativedelta(**{k: v})

    @classmethod
    def get_period(cls, qid: str, period: str,
                   cycle: int, group_by=None) -> list:

        cycle = int(cycle)

        if cycle > 12:  # refuse large data querying
            return []

        period_group_method = {
            'days': lambda d: d.ts.day,
            'weeks': lambda d: d.ts.isocalendar()[1],
            'months': lambda d: d.ts.month,
            'years': lambda d: d.ts.year,
            'seconds': lambda d: d.ts.second,
            'mintues': lambda d: d.ts.timetuple().tm_mn,
            'hours': lambda d: d.ts.timetuple().tm_hour
        }[period]

        def query(start, end) -> [list]:
            grouped = groupby(cls.select(qid, start, end), period_group_method)

            def calcu(data: dict) -> dict:
                ts = max(data.keys())
                df = pandas.DataFrame(data).T.describe()
                res = df.to_dict('index')
                return (ts, res)

            def map2df(g: groupby):  # itertools groupby
                return (calcu(dict(tuple(map(lambda x: (x.ts, x.datum), tail(g))))))

            return tuple(map(map2df, grouped))

        if METRIC.index(period) > 3:
            end = datetime.datetime.now()
            start = cls.shift(end, str(period), int(cycle))
            return query(start, end)
        else:
            dates = list(DateRange(period, cycle))
            return tuple(starmap(cache()(query), dates[:-1])) + (query(*(dates[-1])), )
