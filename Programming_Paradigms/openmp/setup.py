from distutils.core import setup
from distutils.extension import Extension
from Cython.Build import cythonize
import os

ext_modules = [
    Extension(
        "integrate",
        ["integrate.pyx"],
        extra_compile_args=['-fopenmp', '-O3', '-mfma', '-mavx'],
        extra_link_args=['-fopenmp', '-O3', '-mfma', '-mavx'],
    )
]

setup(
    name='integrate-openmp',
    ext_modules = cythonize(ext_modules)
)
