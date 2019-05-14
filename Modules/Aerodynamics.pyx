import logging
import numpy as np
import Atmosphere

logger = logging.getLogger(__name__)

class Drag:
    def __init__(self, diameter):
        logger.debug('Creating Drag Instance')
        self.diameter = diameter
        self.ref_area = self.calc_ref_area(self.diameter)
    
    def get_drag_coefficient(self, vel):
        """
        Get the drag coefficient of the rocket based on the simplified drag model

        :param vel: The velocity of the rocket in mach

        """
        return np.array([0.0, 2400.0 * (np.exp(-1.2*vel[1]) * np.sin(vel[1]) + (vel[1]/6.0) * np.log10(vel[1]+1.0)), 0.0], np.float64)
    
    def get_force(self, vel, pos):
        mach = Atmosphere.ms_to_mach(vel, pos[1])
        c_d = self.get_drag_coefficient(mach)
        density = Atmosphere.get_density(pos[1])
        return 0.5 * density * self.ref_area * np.multiply(c_d, np.power(vel, 2.0))

    def calc_ref_area(self, diameter):
        return np.pi * np.power(diameter/2.0, 2.0)

logger.debug('Aerodynamics Module Loaded')