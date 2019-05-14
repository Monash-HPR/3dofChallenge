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
        return 2400.0 * (np.exp(-1.2*vel) * np.sin(vel) + (vel/6.0) * np.log10(vel+1.0))
    
    def get_force(self, vel, alt):
        mach = Atmosphere.ms_to_mach(vel, alt)
        c_d = self.get_drag_coefficient(mach)
        density = Atmosphere.get_density(alt)
        return 0.5 * c_d * density * self.ref_area * np.power(vel, 2.0)

    def calc_ref_area(self, diameter):
        return np.pi * np.power(diameter/2.0, 2.0)

logger.debug('Aerodynamics Module Loaded')