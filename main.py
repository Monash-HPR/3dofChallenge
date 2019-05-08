import logging

# This should be before the Modules import so the logging level is shared
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

from Modules import Integrator, Aerodynamics, Propulsion, State
logger.debug('All Modules Loaded')

class Simulator:
    def __init__(self):
        logger.debug('Creating Simulator Instance')
        self.motor = Propulsion.Motor()
        self.drag = Aerodynamics.Drag()
        self.state = State.State()

    def initialise(self):
        logger.info('Initialising Simulator')

    def run(self):
        logger.info('Running Simulator')

if __name__ == "__main__":
    logger.info('Starting 3DOF Simulator')
    sim = Simulator()
