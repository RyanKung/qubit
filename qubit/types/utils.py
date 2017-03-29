from collections import namedtuple
import datetime
from dateutil.relativedelta import relativedelta
from itertools import starmap
from operator import mul


__all__ = ['ts_data', 'empty_ts_data', 'DateRange']

ts_data = namedtuple('data', ['datum', 'ts'])


def empty_ts_data():
    return ts_data(datum={}, ts=str(datetime.datetime.now()))


class DateRange():

    def __init__(self, period, cycle, gap=1):
        self.now = datetime.datetime.now()
        self.period = period
        self.gap = gap
        submask = dict(
            years=((1, 0, 0, 0, 0, 0), (1, 1, 1, 0, 0, 0)),
            months=((1, 1, 0, 0, 0, 0), (1, 1, 1, 0, 0, 0)),
            days=((1, 1, 1, 0, 0, 0), (1, 1, 1, 0, 0, 0)),
            hours=((1, 1, 1, 1, 0, 0), (1, 1, 1, 1, 0, 0)),
            minutes=((1, 1, 1, 1, 1, 0), (1, 1, 1, 1, 1, 0)),
            seconds=((1, 1, 1, 1, 1, 1), (1, 1, 1, 1, 1, 1))
        ).get(self.period)

        start_tuple = tuple(
            (self.now - relativedelta(**{period: cycle})).timetuple())[: 6]

        self.start = datetime.datetime(*tuple(starmap(mul, zip(
            starmap(pow, zip(start_tuple, submask[0])), submask[1]))))

    def __call__(self):
        return self

    def __iter__(self):
        return self

    def __str__(self):
        return "<DataRange from: %s to: %s with: %s/%s>" % (
            self.start, self.now, self.period, self.gap)

    def __next__(self):
        if self.start > self.now:
            raise StopIteration('Done')
        start = self.start
        end = start + relativedelta(**{self.period: self.gap})
        if end > self.now:
            res = (start, self.now)
        else:
            res = (start, end)
        self.start = end
        return res
