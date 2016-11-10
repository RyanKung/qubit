from qubit.types import Qubit
from qubit.core import app
from flask import request
from .utils import resp_wrapper as wrapper
from .utils import jsonize


__all__ = ['qubit_api', 'entangle']


@app.route('/qubit/<id>/', methods=['GET', 'DELETE'])
@app.route('/qubit/', methods=['POST'])
@jsonize
@wrapper
def qubit_api(id=None):
    def create():
        return Qubit.create(**request.json)

    def fetch():
        return Qubit.get(id=id)._asdict()

    def update():
        pass

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
