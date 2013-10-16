__author__ = 'zheng'

import numpy
import cPickle

z = numpy.zeros(1000, numpy.uint8)
print len(z.dumps())
print len(cPickle.dumps(z.dumps()))

import zlib, cPickle

def zdumps(obj):
  return zlib.compress(cPickle.dumps(obj,cPickle.HIGHEST_PROTOCOL),9)

def zloads(zstr):
  return cPickle.loads(zlib.decompress(zstr))


print len(zdumps(z))

def pickle(fname, obj):
    import cPickle, gzip
    cPickle.dump(obj=obj, file=gzip.open(fname, "wb", compresslevel=3), protocol=2)

def unpickle(fname):
    import cPickle, gzip
    return cPickle.load(gzip.open(fname, "rb"))