import logging

# This should be before the Modules import so the logging level is shared
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

import Modules.Integrator

if __name__ == "__main__":
    logger.info('Starting 3DOF Simulator')
