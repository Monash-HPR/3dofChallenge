import logging

# This should be before the Modules import so the logging level is shared
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

from Modules import Integrator, Aerodynamics, Propulsion, State

class Simulator:
    def __init__(self):
        logger.debug('Creating Simulator Instance')
        return

    def initialise(self):
        logger.info('Initialising Simulator')
        return
    
    def run(self):
        logger.info('Running Simulator')
        return

if __name__ == "__main__":
    logger.info('Starting 3DOF Simulator')
    sim = Simulator()
