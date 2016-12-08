import datetime
from itertools import groupby
from qubit.types import States
from qubit.core import app
from .utils import resp_wrapper as wrapper
from .utils import jsonize


__all__ = ['states_api', 'states_period_api']


@app.route('/qubit/<id>/from/<start>/to/<end>/', methods=['GET'])
@jsonize
@wrapper
def states_api(id, start, end):
    data = States.select(id, start, end)
    return [d._asdict() for d in data]


@app.route('/qubit/<id>/period/<period>/', methods=['GET'])
@app.route('/qubit/<id>/period/<period>/<cycle>/', methods=['GET'])
@jsonize
@wrapper
def states_period_api(id, period, cycle=1):

    def handler():
        now = datetime.datetime.now()
        print(period, cycle)
        delta_start = datetime.timedelta(**{period: int(cycle)})
        start = now - delta_start
        data = [{k: list(v) for k, v in g}
                for g in groupby(States.select(id, start, now),
                                 lambda x: getattr(x, period[:-1]))]
        return data

    return handler()
