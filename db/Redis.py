import redis


__author__ = 'zheng'


host = '10.7.10.219'
host = 'localhost'
r = redis.StrictRedis(host=host, port=6379, db=0)


def test():
    print r.dbsize()
    # print r.randomkey()
    r.set('image:001', 'iter_001')
    r.set('integer:001', 1)
    for key in r.scan_iter("image:*"):
        print key
    # r.flushdb()  # "Delete all keys in the current database"


def int_out():
    r.set_response_callback('GET', int)
    print "int_out:", r.get('integer:001', 0)


if __name__ == '__main__':
    test()
    int_out()
