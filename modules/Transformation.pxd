cimport numpy as np

cdef np.ndarray c_T_EI (double time)
cdef np.ndarray c_T_GE (np.ndarray pos_g)
cdef np.ndarray c_T_VG (np.ndarray vel_g)
