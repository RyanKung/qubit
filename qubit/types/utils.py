from collections import namedtuple
import datetime

__all__ = ['ts_data', 'empty_ts_data']

ts_data = namedtuple('data', ['datum', 'ts'])

empty_ts_data = ts_data(datum={}, ts=str(datetime.datetime.now()))
