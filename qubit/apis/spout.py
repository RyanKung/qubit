from qubit.core import app
from flask import request


@app.route('/qubit/spout/<name>/', methods=['GET', 'POST', 'UPDATE', 'PUT'])
def spout_api(name):
    def create():
        pass

    def push():
        pass

    def fetch():
        pass

    def update():
        pass

    return {
        'GET': fetch,
        'PUT': push,
        'POST': create
    }.get(request.method)()
