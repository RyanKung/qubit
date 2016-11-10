import json
import datetime
import time
from tests.apis import request
from tests.apis import get


def create_qubit(entangle, name='a qubit'):
    qubit_data = {
        'name': name,
        'entangle': entangle,
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
    end = datetime.datetime.now()
    delta = datetime.timedelta(hours=1)
    start = end - delta
    res = json.loads(get(path='/qubit/%s/from/%s/to/%s/' % (
        qid, str(start), str(end))))
    return len(res['data'])


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
        'body': code,
        'closure': {},
        'rate': 1
    }
    res = json.loads(request(path='/qubit/spout/',
                             data=json.dumps(data), method='POST'))
    assert res['result'] == 'ok'
    res = json.loads(get('/qubit/spout/tester/'))
    assert res['result'] == 'ok'
    # create qubit
    qid = create_qubit('Spout:tester')

    # feed spout
    feed_random_data()
    feed_random_data()
    feed_random_data()

    assert get_hours_data(qid) == 3
    # test entangle
    qid2 = create_qubit('none', 'another')
    entangle(qid2, qid)

    feed_random_data()
    feed_random_data()
    feed_random_data()
    assert get_hours_data(qid2) == 3
    assert get_hours_data(qid) == 6
