import datetime
from qubit.types import States, Qubit
from qubit.core import app
from .utils import resp_wrapper as wrapper
from .utils import jsonize


__all__ = ['states_api']


@app.route('/qubit/<qid>/from/<start>/to/<end>/', methods=['GET'])
@jsonize
@wrapper
def states_api(qid, start, end):
    def format(v):
        if isinstance(v, datetime.datetime):
            return str(v)
        return v

    def strize(d: dict):
        return {k: format(v) for k, v in d._asdict().items()}
    states = Qubit.get(qid)
    data = States.select(states.id, start, end)
    return [strize(d) for d in data]
