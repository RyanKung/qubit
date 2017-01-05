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
        return States.get_period(id, period, cycle)
    return handler()
