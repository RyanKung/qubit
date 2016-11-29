import json
import time
import datetime
from tests.apis import request, get
from operator import sub
from functools import partial


def get_hours_data(qid):
    time.sleep(2)
    end = datetime.datetime.now()
    delta = datetime.timedelta(hours=1)
    start = end - delta
    res = json.loads(get(path='/qubit/%s/from/%s/to/%s/' % (
        qid, str(start), str(end))))
    return res['data']


def test_cpu_case():
    qubit_code = '''
import psutil
from functools import partial

get_rate = partial(psutil.cpu_percent, interval=1)
datum = get_rate()
'''

    qubit_data = {
        'name': 'cpu_example',
        'monad': qubit_code,
        'rate': 100,
        'is_spout': True,
        'is_stem': True,
        'flying': True,
        'store': False,
        'comment': '''The Qubit Sample for testing
 basiclly usage of qubit chains'''
    }
    gen_cpu_qubit = partial(request, path='/qubit/', method='POST', data=json.dumps(qubit_data))

    q1 = json.loads(gen_cpu_qubit())['id']

    another_qubit_data = {
        'name': 'another_qubit',
        'monad': '''
datum = datum
''',
        'entangle': 'Stem:%s' % q1,
        'is_spout': False,
        'is_stem': False,
        'flying': True,
        'store': True,
        'comment': 'another qubit'
    }
    gen_another_qubit = partial(request, path='/qubit/', method='POST', data=json.dumps(another_qubit_data))

    q2 = json.loads(gen_another_qubit())['id']
    assert sub(int(q2), int(q1)) == 1
    time.sleep(10)
    data1 = get_hours_data(q1)
    data2 = get_hours_data(q2)
    assert len(data1) == 0
    assert len(data2) > 5
