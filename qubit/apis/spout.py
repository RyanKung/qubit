from qubit.types import Spout
from qubit.core import app
from flask import request
from .utils import resp_wrapper as wrapper
from .utils import jsonize

__all__ = ['spout_api']


@app.route('/qubit/spout/<name>/', methods=['GET', 'UPDATE', 'PUT'])
@app.route('/qubit/spout/', methods=['POST'])
@jsonize
@wrapper
def spout_api(name=None):
    def create():
        data = request.json
        return Spout.create(**data)

    def push():
        pass

    def fetch():
        return Spout.get_via_name(name=name)

    def update():
        pass

    return {
        'GET': fetch,
        'PUT': push,
        'POST': create
    }.get(request.method)()
