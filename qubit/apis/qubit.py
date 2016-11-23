from qubit.types import Qubit
from qubit.types.utils import ts_data
from qubit.core import app
from flask import request
from .utils import resp_wrapper as wrapper
from .utils import jsonize


__all__ = ['qubit_api', 'entangle', 'stem_api']


@app.route('/qubit/<name>/', methods=['GET', 'DELETE'])
@app.route('/qubit/', methods=['POST'])
@jsonize
@wrapper
def qubit_api(name=None):
    def create():
        return dict(id=Qubit.create(**request.json))

    def push():
        qubit = Qubit.get_by(name=name)
        data = ts_data(**request.json)
        Qubit.measure(qubit, data)

    def fetch():
        res = Qubit.get_via_name(name=name)
        return res and res._asdict()

    def update():
        return Qubit.update(name=name, **request.json)

    def delete():
        return Qubit.manager.delete_by(name=name)
    return {
        'GET': fetch,
        'PUT': push,
        'DELETE': delete,
        'POST': create
    }.get(request.method)()


@app.route('/qubit/stem/', methods=['GET', 'POST'])
@jsonize
@wrapper
def stem_api(name=None):
    def get():
        stems = Qubit.get_stem()
        return stems and list(map(lambda x: x._asdict(), stems))
    return {
        'GET': get
    }.get(request.method)()


@app.route('/qubit/<name>/last/', methods=['GET'])
@jsonize
@wrapper
def last(name):
    return Qubit.get_current(name)


@app.route('/qubit/entangle/<qid>/', methods=['POST'])
@jsonize
@wrapper
def entangle(qid):
    data = request.json
    return Qubit.entangle(qid, data['id'])
