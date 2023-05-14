# cython: boundscheck=False
# cython: wraparound=False
# cython: nonecheck=False
# cython: cdivision=True

from __future__ import division
import numpy as np
cimport numpy as np
from cython.parallel cimport prange
cimport openmp
from cython.view cimport array as cvarray
cimport cython

float32 = np.float32
ctypedef np.float32_t float32_t

def sum_0(vecs):
	"""
	numpy baseline
	"""
	return np.sum(vecs, axis=0)

def sum_01(vecs):
	"""
	numpy baseline
	"""
	sum_vec = np.zeros(vecs.shape[1]).astype(np.float32)
	for i in range(vecs.shape[0]):
		sum_vec += vecs[i]
	return sum_vec

def sum_1(np.ndarray[float32_t, ndim=2] vecs):
	"using buffer test"
	cdef int M = vecs.shape[0]
	cdef int N = vecs.shape[1]
	cdef np.ndarray[float32_t, ndim=1] results = np.zeros(N, dtype=np.float32)
	cdef int i, j
	cdef float32_t value = 0	
	for i in range(M):
		value = 0
		for j in range(N):
			value += vecs[i, j]
		results[i] = value
	return results

def sum_2(float32_t[:,:] vecs):
	"using view test"
	cdef int M = vecs.shape[0]
	cdef int N = vecs.shape[1]
	cdef float32_t[:] results = np.zeros(N, dtype=np.float32)
	cdef int i, j
	cdef float32_t value = 0
	for i in range(M):
		value = 0
		for j in range(N):
			value += vecs[i, j]
		results[i] = value
	return results

@cython.boundscheck(False)
@cython.wraparound(False)
def sum_3(float32_t[:,:] vecs):
	"using view test with uncheck"
	cdef int M = vecs.shape[0]
	cdef int N = vecs.shape[1]
	cdef float32_t[:] results = np.zeros(N, dtype=np.float32)
	cdef int i, j
	cdef float32_t value = 0
	for i in range(M):
		value = 0
		for j in range(N):
			value += vecs[i, j]
		results[i] = value
	return results

@cython.boundscheck(False)
@cython.wraparound(False)
def sum_4(float32_t[:,:] vecs):
	"using buffer test"
	cdef int M = vecs.shape[0]
	cdef int N = vecs.shape[1]
	cdef float32_t[:] results = np.zeros(N, dtype=np.float32)
	cdef int i, j
	cdef float32_t value = 0
	for i in range(M):
		value = 0
		for j in prange(N, nogil = True):
			value += vecs[i, j]
		results[i] = value
	return results

@cython.boundscheck(False)
@cython.wraparound(False)
def sum_5(float32_t[:,:] vecs):
	"using buffer test"
	cdef int M = vecs.shape[0]
	cdef int N = vecs.shape[1]
	cdef float32_t[:] results = np.zeros(N, dtype=np.float32)
	cdef int i, j
	cdef float32_t value = 0
	for i in range(M):
		value = 0
		for j in prange(N, nogil = True, num_threads=6):
			value += vecs[i, j]
		results[i] = value
	return results

@cython.boundscheck(False)
@cython.wraparound(False)
def sum_7(float32_t[:,:] vecs):
	"using buffer test"
	cdef int M = vecs.shape[0]
	cdef int N = vecs.shape[1]
	cdef float32_t[:] results = np.zeros(N, dtype=np.float32)
	cdef int i, j
	cdef float32_t value = 0
	for i in prange(M, nogil = True):
		for j in prange(N):
			results[i] += vecs[i, j]
	return results

@cython.boundscheck(False)
@cython.wraparound(False)
def sum_6(float32_t[:,:] vecs):
	"using buffer test"
	cdef int M = vecs.shape[0]
	cdef int N = vecs.shape[1]
	cdef float32_t[:] results = np.zeros(N, dtype=np.float32)
	cdef int i, j
	cdef float32_t value = 0
	for i in prange(M, nogil = True):
		for j in range(N):
			results[i] += vecs[i, j]
	return results

