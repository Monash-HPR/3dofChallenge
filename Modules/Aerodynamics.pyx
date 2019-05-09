import logging
import numpy as np
import Atmosphere

logger = logging.getLogger(__name__)

class Drag:
    def __init__(self, diameter):
        logger.debug('Creating Drag Instance')
        self.diameter = diameter
        self.ref_area = self.calc_ref_area(self.diameter)
    
    def get_drag_coefficient(self, M):
        return 2400 * (np.exp(-1.2*M) * np.sin(M) + (M/6) * np.log10(M+1))
    
    def get_drag_force(self, state):
        mach = Atmosphere.ms_to_mach(state.vel)
        c_d = self.get_drag_coefficient(mach)
        density = Atmosphere.get_density(state.alt)
        return 0.5 * c_d * density * self.ref_area * np.power(state.vel, 2)
    
    def calc_ref_area(self, diameter):
        return np.pi * np.power(diameter/2, 2)

logger.debug('Aerodynamics Module Loaded')