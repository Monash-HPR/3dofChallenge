import logging
import numpy as np
import Atmosphere

logger = logging.getLogger(__name__)

class Drag:
    def __init__(self, diameter):
        logger.debug('Creating Drag Instance')
        self.diameter = diameter
        self.ref_area = self.calc_ref_area(self.diameter)
    
    @staticmethod
    def get_drag_coefficient(vel):
        """
        Get the drag coefficient of the rocket based on the simplified drag model

        :param vel: The velocity of the rocket in mach (w.r.t. Earth)

        """
        #return np.array([0.0, 2400.0 * (np.exp(-1.2*vel[1]) * np.sin(vel[1]) + (vel[1]/6.0) * np.log10(vel[1]+1.0)), 0.0], np.float64)
        return np.array([
            0.0,
            np.exp(-0.5 * vel[1])
            * (
                0.5*np.exp(-2.0*vel[1])
                 * np.cos(5.5 * vel[1])
                + 0.1*vel[1]
                 * np.log(np.abs(vel[1])+0.01) + 0.5
            )
             + 0.1*np.exp(vel[1] - 5),
            0.0
        ], np.float64)
    
    def get_force(self, vel, pos):
        mach = Atmosphere.ms_to_mach(vel, pos[1])
        c_d = np.abs(self.get_drag_coefficient(mach))
        density = Atmosphere.get_density(pos[1])
        dynamic_pressure = 0.5 * density * np.power(vel, 2.0)

        # Magnitude of the drag force from the drag equation
        force_abs = self.ref_area * np.multiply(c_d, dynamic_pressure)

        # Make sure the drag force acts in the opposite direction to the velocity
        return np.multiply(-np.sign(vel), force_abs)

    @staticmethod
    def calc_ref_area(diameter):
        return np.pi * np.power(diameter/2.0, 2.0)

logger.debug('Aerodynamics Module Loaded')
