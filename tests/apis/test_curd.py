import json
import datetime
import time
from tests.apis import request
from tests.apis import get


def create_qubit(entangle, name='a qubit'):
    qubit_data = {
        'name': name,
        'entangle': entangle
    }
    res = json.loads(request(path='/qubit/', data=json.dumps(qubit_data), method='POST'))
    assert res['result'] == 'ok'
    qid = res['id']
    return qid


def entangle(q1, q2):
    res = json.loads(request(path='/qubit/entangle/%s/' % q1, data=json.dumps({
        'id': q2
    }), method='POST'))
    assert res['result'] == 'ok'
    return res


def get_hours_data(qid):
    time.sleep(2)
    end = datetime.datetime.now()
    delta = datetime.timedelta(hours=1)
    start = end - delta
    res = json.loads(get(path='/qubit/%s/from/%s/to/%s/' % (
        qid, str(start), str(end))))
    return res['data']


def feed_random_data(spout='tester'):
    data = {
        'datum': {
            'a': time.time()
        },
        'ts': str(datetime.datetime.now())
    }
    res = json.loads(request(path='/qubit/spout/%s/' % spout,
                             data=json.dumps(data), method='PUT'))
    assert res['result'] == 'ok'


def test_crud():
    code = '1'
    data = {
        'name': 'tester',
        'monad': code,
        'rate': 1
    }
    res = json.loads(request(path='/qubit/',
                             data=json.dumps(data), method='POST'))
    assert res['result'] == 'ok'
