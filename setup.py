from distutils.core import setup
from Cython.Build import cythonize
import numpy as np

if __name__ == "__main__":
  setup(
  name='3DOF - Kenneth',
  ext_modules = cythonize( "modules/**/*.pyx",
                           build_dir="build",
                           nthreads=4,
                           compiler_directives={'boundscheck': False,
                                                'cdivision': True,
                                                'profile': True,   # Set to true when profiling for better info.
                                                'infer_types': True,
                                                'language_level': '3'}),
    include_dirs = [np.get_include()]
)
