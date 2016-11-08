import celery
from typing import NamedTuple

PeriodTask = NamedTuple('PeriodTask', [
    ('period', int),
    ('task', celery.Task),
    ('name', str)
])
