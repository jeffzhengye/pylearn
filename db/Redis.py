__author__ = 'zheng'

import redis
host = '10.7.10.219'
r = redis.StrictRedis(host=host, port=6379, db=0)
print r.dbsize()
print r.randomkey()
#r.flushdb()