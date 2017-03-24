import asyncio
import asyncpg
from pulsar import ensure_future
from typing import Callable


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


async def async_call(sql):
    method = sql.split(' ')[0]
    conn = await asyncpg.connect(host=PGSQL_PARAM['host'],
                                 user=PGSQL_PARAM['user'],
                                 database=PGSQL_PARAM['database'],
                                 port=PGSQL_PARAM['port'])
    res = await {
        'SELECT': conn.fetch,
        'INSERT': conn.fetchval,
        'UPDATE': conn.execute
    }.get(method, conn.execute)(sql)
    return res


pool = psycopg2.pool.SimpleConnectionPool(1, 60 * 1000, **PGSQL_PARAM)
