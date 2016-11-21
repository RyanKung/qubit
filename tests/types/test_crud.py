from qubit.types import Qubit


def test_qubit():
    data = {
        'name': 'test_qubit',
        'entangle': 'Spout:tester',
        'flying': True
    }
    Qubit.create(**data)
