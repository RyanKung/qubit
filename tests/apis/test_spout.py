import json
import datetime
import time
from tests.apis import request
from tests.apis import get


def test_crud():
    code = '1'
    data = {
        'name': 'tester',
        'body': code,
        'closure': {},
        'rate': 1
    }
    res = json.loads(request(path='/qubit/spout/',
                             data=json.dumps(data), method='POST'))
    assert res['result'] == 'ok'
    res = json.loads(get('/qubit/spout/tester/'))
    assert res['result'] == 'ok'
    data = {
        'datum': {
            'a': time.time()
        },
        'ts': str(datetime.datetime.now())
    }
    res = json.loads(request(path='/qubit/spout/tester/',
                             data=json.dumps(data), method='PUT'))
    assert res['result'] == 'ok'
