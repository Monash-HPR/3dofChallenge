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
        :param accel_func:
        :type accel_func: Callable with 2 arguments (time, alt)

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
        k_vel = np.zeros(length + 1) # vels
        k_acc = np.zeros(length + 1) # acc

        # Calculate the estimates
        for i in range(1,length+1):
            _time = state.time + c[i]*self.h
            _alt = state.alt + self.h*np.sum(np.multiply(a[i], k_vel))
            k_vel[i] = state.vel + self.h*np.sum(np.multiply(a[i], k_acc))
            k_acc[i] = accel_func(_time, k_vel[i], _alt)

        # Reduce the estimates to a single set of values
        t_final = state.time + self.h
        alt_final = state.alt + self.h*np.sum(np.multiply(b, k_vel))
        vel_final = state.vel + self.h*np.sum(np.multiply(b, k_acc))
        acc_final = (vel_final - state.vel)/self.h
        return state.update(
            time=t_final,
            alt=alt_final,
            vel=vel_final,
            acc=acc_final
        )

logger.debug('Integrator Module Loaded')