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
        :type accel_func: Callable with 3 arguments (time, vel, alt)

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
        k_vel = np.zeros((length + 1, 3)) # vels
        k_acc = np.zeros((length + 1, 3)) # acc

        # Calculate the estimates
        for i in range(1,length+1):
            _time = state.time + c[i]*self.h
            _pos = state.pos + self.h*np.sum(np.multiply(k_vel.T, a[i]).T)
            k_vel[i] = state.vel + self.h*np.sum(np.multiply(k_acc.T, a[i]).T)
            k_acc[i] = accel_func(_time, k_vel[i], _pos)

        # Reduce the estimates to a single set of values
        t_final = state.time + self.h
        delta_pos = self.h*np.sum(np.multiply(k_vel.T, b).T, 0)
        pos_final = state.pos + delta_pos
        delta_v = self.h*np.sum(np.multiply(k_acc.T, b).T, 0)
        vel_final = state.vel + delta_v
        acc_final = np.divide(delta_v, self.h)
        return state.update(
            time=t_final,
            pos=pos_final,
            vel=vel_final,
            acc=acc_final
        )

logger.debug('Integrator Module Loaded')