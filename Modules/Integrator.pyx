import logging
cimport numpy as np
import numpy as np

logger = logging.getLogger(__name__)

class Integrator:
    def __init__(self, step):
        logger.debug('Creating Integrator Instance')
        self.h = step

    def RK4(self, state, accel_func):
        """
        RK4 method used for integrating

        :param state: The current state to use
        :type state: Modules.State.State
        :param accel_func: Function to return the acceleration of the body w.r.t. the inertial frame
        :type accel_func: Callable with 3 arguments (time, vB_E_I, sBE__I)

        """
        # Number of estimates the method uses
        length = 4

        # The method's constants
        a = np.array([
            [0,   0,   0,  0,  0],
            [0,   0,   0,  0,  0],
            [0, 0.5,   0,  0,  0],
            [0,   0, 0.5,  0,  0],
            [0,   0,   0,  1,  0]
        ], dtype=np.float64)
        b = np.array([0.0, 1.0/6.0, 1.0/3.0, 1.0/3.0, 1.0/6.0], dtype=np.float64)
        c = np.array([0.0, 0.0, 0.5, 0.5, 1.0], dtype=np.float64)

         # Number of estimates + 1 (0-indexed arrays)
        vB_E_I_k = np.zeros((length + 1, 3)) # vels
        aB_E_I_k = np.zeros((length + 1, 3)) # acc

        # Calculate the estimates
        for i in range(1,length+1):
            time_est = state.time + c[i]*self.h
            sBE__I_est = state.pos + self.h*np.sum(np.multiply(vB_E_I_k.T, a[i]).T)
            vB_E_I_k[i] = state.vel + self.h*np.sum(np.multiply(aB_E_I_k.T, a[i]).T)
            aB_E_I_k[i] = accel_func(time_est, vB_E_I_k[i], sBE__I_est)

        # Reduce the estimates to a single set of values
        t_final = state.time + self.h
        delta_pos = self.h*np.sum(np.multiply(vB_E_I_k.T, b).T, 0)
        sBE__I_est = state.pos + delta_pos
        delta_v = self.h*np.sum(np.multiply(aB_E_I_k.T, b).T, 0)
        vB_E_I_est = state.vel + delta_v
        aB_E_I_est = np.divide(delta_v, self.h)
        return state.update(
            time=t_final,
            pos=sBE__I_est,
            vel=vB_E_I_est,
            acc=aB_E_I_est
        )

logger.debug('Integrator Module Loaded')