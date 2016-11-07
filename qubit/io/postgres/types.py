from typing import NamedTuple
from typing import NewType

__all__ = ['json', 'varchar',
           'boolean', 'Table']

json = NewType('json', dict)
varchar = NewType('varchar', str)
boolean = NewType('boolean', bool)
text = NewType('text', str)

Table = NamedTuple
