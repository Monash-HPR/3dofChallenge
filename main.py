import logging

# This should be before the Modules import so the logging level is shared
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

from Modules import Integrator, Aerodynamics, Propulsion, State, Atmosphere
logger.debug('All Modules Loaded')

class Simulator:
    def __init__(self, diameter):
        logger.debug('Creating Simulator Instance')

        self.diameter = diameter
        self.motor = Propulsion.BasicMotor(
            average_thrust=839.0,
            propellant_mass=4.436,
            burnout_time=8.96,
            casing_mass=2.518
        )
        self.drag = Aerodynamics.Drag(diameter=self.diameter)
        self.state = State.State()

    def initialise(self):
        logger.info('Initialising Simulator')

    def run(self):
        logger.info('Running Simulator')

if __name__ == "__main__":
    logger.info('Starting 3DOF Simulator')
    sim = Simulator(
        diameter=0.1
    )
