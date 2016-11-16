from qubit.types import Qubit
from qubit.core import app
from flask import request
from .utils import resp_wrapper as wrapper
from .utils import jsonize


__all__ = ['qubit_api', 'entangle', 'mapper_api', 'reducer_api']


@app.route('/qubit/<id>/', methods=['GET', 'DELETE'])
@app.route('/qubit/', methods=['POST'])
@jsonize
@wrapper
def qubit_api(id=None):
    def create():
        return dict(id=Qubit.create(**request.json))

    def fetch():
        return Qubit.get(id=id)._asdict()

    def update():
        pass

    def delete():
        return Qubit.delete(id)

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


@app.route('/qubit/<qid>/mapper/<mid>/', methods=['PUT'])
@jsonize
@wrapper
def mapper_api(qid, mid):
    return Qubit.add_mapper(qid, mid)


@app.route('/qubit/<qid>/reducer/<rid>/', methods=['PUT', 'DELETE'])
@jsonize
@wrapper
def reducer_api(qid, rid):
    def add():
        return Qubit.add_reducer(qid, rid)

    def remove():
        return Qubit.delete_reducer(qid, rid)

    return {
        'PUT': add,
        'DELETE': remove
    }.get(request.method)()
