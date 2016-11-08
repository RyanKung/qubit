__all__ = ['PGSQL_PARAM', 'MQ_BROKER', 'REDIS_BACKEND']

PGSQL_PARAM = dict(user='ryan',
                   host='127.0.0.1',
                   database='qubit',
                   port=5432)

MQ_PARAMS = {"host": "127.0.0.1", "port": 5672}
REDIS_PARMAS = {"host": "127.0.0.1", "port": 6379}
REDIS_BACKEND = "redis://%s:%s" % (REDIS_PARMAS['host'], REDIS_PARMAS['port'])
MQ_BROKER = "amqp://%s:%s//" % (MQ_PARAMS['host'], MQ_PARAMS['port'])
