"""
click to see in which directory the libc.stdlib is
/usr/local/lib/python2.7/dist-package/Cython/Includes
"""
from libc.stdlib cimport malloc, free # C std library


cimport numpy as cnp # numpy c-api
from libcpp.vector cimport vector # c++ std::vector

