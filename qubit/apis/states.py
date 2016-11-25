import datetime
from qubit.types import States
from qubit.core import app
from .utils import resp_wrapper as wrapper
from .utils import jsonize


__all__ = ['states_api']


@app.route('/qubit/<name>/from/<start>/to/<end>/', methods=['GET'])
@jsonize
@wrapper
def states_api(name, start, end):
    def format(v):
        if isinstance(v, (int, str, float)):  # cover unixtimestamp to datetime string
            return str(datetime.datetime.fromtimestamp(float(v)))
        if isinstance(v, datetime.datetime):
            return str(v)
        return v

    def strize(d: dict):
        return {k: format(v) for k, v in d._asdict().items()}
    data = States.select(name, start, end)
    return [strize(d) for d in data]
