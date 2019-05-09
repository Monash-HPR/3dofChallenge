import logging
import numpy as np

logger = logging.getLogger(__name__)

class Motor:
    def __init__(self, average_thrust, propellant_mass, burnout_time, casing_mass):
        """
        Initialise a new Motor instance

        """
        logger.debug('Creating Motor Instance')

        self.average_thrust = average_thrust
        self.propellant_mass = propellant_mass
        self.burnout_time = burnout_time
        self.casing_mass = casing_mass

    def get_mass(self, time):
        """
        Get the motor mass at a given time.

        Assumes a linear mass decrease.

        :param time: The time in seconds
        :type time: float
        :returns: The mass in kilograms of the motor at the given time

        """
        if time > self.burnout_time:
            return self.casing_mass
        
        return self.casing_mass + self.propellant_mass - (self.propellant_mass*time)/self.burnout_time
    
    def get_thrust(self, time):
        """
        Get the motor thrust at a given time.

        Assumes a constant thrust for the duration of the motor burn.

        :param time: The time in seconds
        :returns: The motor thrust in Newtons at the given time
        """
        return self.average_thrust if time < self.burnout_time else 0

logger.debug('Propulsion Module Loaded')