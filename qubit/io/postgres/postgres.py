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

connection = psycopg2.connect(**PGSQL_PARAM)
# for creat a new connection
pool = psycopg2.pool.SimpleConnectionPool(5, 50, **PGSQL_PARAM)
