import json
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
    res = json.loads(request(path='/qubit/spout/', data=json.dumps(data), method='POST'))
    assert res['result'] == 'ok'
    res = json.loads(get('/qubit/spout/tester/'))
    print(res)
    assert res['result'] == 'ok'
