import logging

logger = logging.getLogger(__name__)

class Integrator:
    def __init__(self, step):
        logger.debug('Creating Integrator Instance')
        self.step = step

    def RK4(self):
        return

logger.debug('Integrator Module Loaded')