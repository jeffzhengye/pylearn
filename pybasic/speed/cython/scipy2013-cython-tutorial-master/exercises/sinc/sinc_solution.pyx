from libc.math cimport sin

cpdef double sinc_kernel(double x):
    if -0.01 < x < 0.01:
        return 1.0
    return sin(x) / x
