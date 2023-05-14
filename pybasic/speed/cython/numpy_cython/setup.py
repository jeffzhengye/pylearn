from distutils.core import setup
from distutils.extension import Extension
from Cython.Distutils import build_ext


exts = [Extension("convolve1", ["convolve1.pyx"]),
        Extension("convolve2", ["convolve2.pyx"]),
        Extension("convolve3", ["convolve3.pyx"]),
        Extension("convolve4", ["convolve4.pyx"]),
        Extension("numpy_array_sum", ["numpy_array_sum.pyx"],
        	  libraries=["m"],
              extra_compile_args = ["-O3", "-ffast-math", "-march=native", "-fopenmp" ],
              extra_link_args=['-fopenmp']
        	),
        ]

setup(
    cmdclass = {'build_ext': build_ext},
    ext_modules = exts,
)
