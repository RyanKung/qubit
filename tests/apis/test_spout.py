import json
from tests.apis import request
from tests.apis import get


def test_spout():
    get_depth = '(lambda m: m.HuoBi(m.access_key, m.secret_key))(__import__("pro.huobi").huobi).get_depth()'
    code = get_depth
    data = {
        'name': 'import_tester',
        'body': code,
        'rate': 1
    }
    res = json.loads(request(path='/qubit/spout/',
                             data=json.dumps(data), method='POST'))
    assert res['result'] == 'ok'
    res = json.loads(get('/qubit/spout/tester/last/'))
