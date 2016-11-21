from qubit.types import Spout
from qubit.types import Qubit

def test_spout():
    code = '1'
    data = {
        'name': 'test_spout',
        'body': code,
        'rate': 1
    }
    Spout.create(**data)


def test_qubit():
    data = {
        'name': 'test_qubit',
        'entangle': 'Spout:tester',
        'flying': True
    }
    Qubit.create(**data)
