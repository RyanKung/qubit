from functools import partial
import postgresql
from qubit.config import PGSQL_PARAM

__all__ = ['connection', 'new_connection']

connection = postgresql.open(**PGSQL_PARAM)
# for creat a new connection
new_connection = partial(postgresql.open, **PGSQL_PARAM)
