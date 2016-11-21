from qubit.types import Qubit
from qubit.types.utils import ts_data
from qubit.core import app
from flask import request
from .utils import resp_wrapper as wrapper
from .utils import jsonize


__all__ = ['qubit_api', 'entangle']


@app.route('/qubit/<name>/', methods=['GET', 'DELETE'])
@app.route('/qubit/', methods=['POST'])
@jsonize
@wrapper
def qubit_api(name=None):
    def create():
        return dict(id=Qubit.create(**request.json))

    def push():
        qubit = Qubit.get_via_name(name=name)
        data = ts_data(**request.json)
        Qubit.measure(qubit, data)

    def fetch():
        return Qubit.get(id=id)._asdict()

    def update():
        return Qubit.update(name=name, **request.json)

    def delete():
        return Qubit.manager.delete_by(name=name)

    return {
        'GET': fetch,
        'POST': create
    }.get(request.method)()


@app.route('/qubit/entangle/<qid>/', methods=['POST'])
@jsonize
@wrapper
def entangle(qid):
    data = request.json
    return Qubit.entangle(qid, data['id'])
