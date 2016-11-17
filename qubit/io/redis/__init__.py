import redis
from qubit.config import REDIS_PARMAS

__all__ = ['kv_client']

kv_client = redis.StrictRedis(**REDIS_PARMAS)
