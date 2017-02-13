from qubit.types import Qubit
from qubit.types.utils import ts_data
from qubit.core import app
from flask import request
from .utils import resp_wrapper as wrapper
from .utils import jsonize


__all__ = ['qubit_api', 'entangle', 'stem_api', 'monad_tester']


@app.route('/qubit/<qid>/', methods=['GET', 'DELETE', 'PATCH'])
@app.route('/qubit/', methods=['POST'])
@jsonize
@wrapper
def qubit_api(qid=None):
    def create():
        return dict(id=Qubit.create(**request.json))

    def push():
        qubit = Qubit.get(qid)
        data = ts_data(**request.json)
        Qubit.measure(qubit, data)

    def fetch():
        res = Qubit.get(qid)
        return res and res._asdict()

    def update():
        return Qubit.update(qid, request.json)

    def delete():
        return Qubit.manager.delete(qid)

    return {
        'GET': fetch,
        'PUT': push,
        'PATCH': update,
        'DELETE': delete,
        'POST': create
    }.get(request.method)()


@app.route('/qubit/monad/test/', methods=['POST'])
@jsonize
@wrapper
def monad_tester():
    loc = {}
    try:
        Qubit.exec_monad(request.json['monad'], loc=loc)
        return dict(data=loc)
    except Exception as e:
        return {
            'data': dict(ex=e)
        }


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


@app.route('/qubit/<qid>/last/', methods=['GET'])
@jsonize
@wrapper
def last(qid):
    return Qubit.get_current(qid)


@app.route('/qubit/entangle/<entangle>/', methods=['GET'])
@app.route('/qubit/entangle/<qid>/', methods=['POST'])
@jsonize
@wrapper
def entangle(qid=None, entangle=None):
    def set_entangle():
        data = request.json
        return Qubit.entangle(qid, data['id'])

    def get_entangle():
        return list(map(lambda x: x, Qubit.get_flying(entangle)))

    return {
        'GET': get_entangle,
        'POST': set_entangle
    }.get(request.method)()


@app.route('/qubit/entangle/<entangle>/tree/', methods=['GET'])
@jsonize
@wrapper
def entangle_tree(entangle):
    def get_entangle_tree(entangle):
        res = [list(map(lambda x: x, Qubit.get_flying(entangle)))]
        return res or res + list(map(get_entangle_tree, res))
    return get_entangle_tree(entangle)
