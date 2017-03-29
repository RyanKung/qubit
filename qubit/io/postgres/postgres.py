# -*- eval: (venv-workon "qubit"); -*-

import asyncpg
from flask import request

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
    if not getattr(async_call, 'conn', None):
        conn = await asyncpg.connect(
            host=PGSQL_PARAM['host'],
            user=PGSQL_PARAM['user'],
            database=PGSQL_PARAM['database'],
            port=PGSQL_PARAM['port'])
        async_call.conn = conn

    res = await {
        'SELECT': async_call.conn.fetch,
        'INSERT': async_call.conn.fetchval,
        'UPDATE': async_call.conn.fetchval
    }.get(method, async_call.conn.execute)(sql)
    return res


pool = psycopg2.pool.SimpleConnectionPool(1, 60 * 1000, **PGSQL_PARAM)


async def async_call_with_pool(sql, pool):
    method = sql.split(' ')[0]
    async with pool:
        async with pool.acquire() as conn:
            res = await {
                'SELECT': conn.fetch,
                'INSERT': conn.fetchval,
                'UPDATE': conn.fetchval
            }.get(method, conn.execute)(sql)
            return res


class PostgresMiddleware():
    def __init__(self):
        self.pool = asyncpg.create_pool(
            host=PGSQL_PARAM['host'],
            user=PGSQL_PARAM['user'],
            database=PGSQL_PARAM['database'],
            port=PGSQL_PARAM['port'])

    def __call__(self, environ, start_response=None):
        environ['PG_POOL'] = self.pool
        return None
