import logging
import numpy as np

logger = logging.getLogger(__name__)

class Motor:
    """
    The basic Motor class that all other motor subclasses inherit from.

    """
    def __init__(self, burnout_time, casing_mass):
        """
        Initialise a new Motor instance

        """
        logger.debug('Creating Motor Instance')

        self.burnout_time = burnout_time
        self.casing_mass = casing_mass

    def get_mass(self, time):
        """
        Method for getting the mass of the motor at a given time.
        
        This method is not explicitly declared here, and should be declared in the subclass.
        """
        logger.error('Mass method not implemented. Ensure a subclass is being used and the Motor class is not being instantiated directly.')
        raise NotImplementedError
    
    def get_thrust(self, time):
        """
        Method for getting the thrust of the motor at a given time.
        
        This method is not explicitly declared here, and should be declared in the subclass.
        """
        logger.error('Thrust method not implemented. Ensure a subclass is being used and the Motor class is not being instantiated directly.')
        raise NotImplementedError

class BasicMotor(Motor):
    """
    A Motor with constant thrust and constant rate of mass decrease.

    """
    def __init__(self, average_thrust, burnout_time, propellant_mass=None, casing_mass=None, total_mass=None):
        """
        Initialise a new Basic Motor instance

        """
        logger.debug('Creating Basic Motor Instance')

        if propellant_mass and casing_mass and total_mass:
            if propellant_mass == total_mass - casing_mass:
                logger.warning('All 3 masses set for motor, but values match so simulation can continue.')
            else:
                logger.error('All 3 masses set for motor, and values do not match.')
                raise ValueError('All 3 masses set for motor, and values do not match.')

        if propellant_mass and casing_mass:
            # Total mass is not needed, but make sure no error is raised when it isn't set
            pass
        elif casing_mass and total_mass:
            # Get the mass of the propellant
            propellant_mass = total_mass - casing_mass
        elif propellant_mass and total_mass:
            # Get the mass of the casing
            casing_mass = total_mass - propellant_mass
        else:
            logger.error('Not enough values supplied to motor instantiation. 2 of the 3 mass values must be supplied.')

        super().__init__(burnout_time, casing_mass)

        self.average_thrust = average_thrust
        self.propellant_mass = propellant_mass

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