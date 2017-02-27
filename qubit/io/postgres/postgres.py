try:
    import psycopg2
    import psycopg2.pool
except:
    from psycopg2cffi import compat
    compat.register()
    import psycopg2
    import psycopg2.pool
from qubit.config import PGSQL_PARAM

__all__ = ['connection', 'pool']


def connection():
    if not getattr(connection, '_conn', None):
        connection._conn = psycopg2.connect(**PGSQL_PARAM)
    return connection._conn
# for creat a new connection
pool = psycopg2.pool.SimpleConnectionPool(1, 60 * 1000, **PGSQL_PARAM)
