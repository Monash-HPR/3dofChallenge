from distutils.core import setup
from Cython.Build import cythonize

setup(name='3DOF', ext_modules=cythonize("Modules/*.pyx"))
