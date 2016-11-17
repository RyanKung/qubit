from qubit.types import Spout
from qubit.types.utils import ts_data
from qubit.core import app
from flask import request
from .utils import resp_wrapper as wrapper
from .utils import jsonize


__all__ = ['spout_api', 'spout_data']


@app.route('/qubit/spout/<name>/', methods=['GET', 'UPDATE', 'PUT', 'DELETE'])
@app.route('/qubit/spout/', methods=['POST', 'GET'])
@jsonize
@wrapper
def spout_api(name=None):

    def create():
        return Spout.create(**request.json)

    def push():
        spout = Spout.get_via_name(name=name)
        data = ts_data(**request.json)
        Spout.measure(spout, data)

    def fetch():
        if name:
            data = Spout.get_via_name(name=name)._asdict()
        else:
            data = Spout.get_list()
        return data

    def update():
        return Spout.update(name=name, **request.json)

    def delete():
        return Spout.manager.delete(name=name)

    return {
        'GET': fetch,
        'PUT': push,
        'POST': create,
        'DELETE': delete
    }.get(request.method)()


@app.route('/qubit/spout/<name>/last/', methods=['GET'])
@jsonize
@wrapper
def spout_data(name):
    spout = Spout.get_via_name(name)
    res = Spout.get_status(spout)._asdict()
    res['ts'] = str(res['ts'])
    return res
