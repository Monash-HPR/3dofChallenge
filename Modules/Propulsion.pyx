import logging
cimport numpy as np

logger = logging.getLogger(__name__)

class Motor:
    def __init__(self):
        logger.debug('Creating Motor Instance')

        self.initial_mass = 0
        self.burnout_time = 0
        self.average_thrust = 0

    def get_mass(self, time):
        return
    
    def get_thrust(self, time):
        return self.average_thrust if time < self.burnout_time else 0

logger.debug('Propulsion Module Loaded')