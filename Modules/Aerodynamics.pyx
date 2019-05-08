import logging
cimport numpy as np

logger = logging.getLogger(__name__)

class Drag:
    def __init__(self):
        logger.debug('Creating Drag Instance')
    
    def get_drag_coefficient(self, mach):
        return 2400 * (np.exp(-1.2*M) * np.sin(M) + (M/6) * np.log10(M+1))

logger.debug('Aerodynamics Module Loaded')