# Code for Cython compiler
from distutils.core import setup
from Cython.Build import cythonize
import numpy

setup(
    name = "3DoF Sim",
    ext_modules = cythonize("Modules/*.pyx"),
    include_dirs = [numpy.get_include()]
)
