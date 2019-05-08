import logging

logger = logging.getLogger(__name__)

class State:
    def __init__(self, **kwargs):
        logger.debug('Creating State Instance')
        self.time = kwargs.get('time', 0)
        self.altitude = kwargs.get('altitude', 0)
        self.velocity = kwargs.get('velocity', 0)

logger.debug('State Module Loaded')