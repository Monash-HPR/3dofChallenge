import json
import logging

logger = logging.getLogger(__name__)

class State:
    def __init__(self, **kwargs):
        logger.debug('Creating State Instance')
        self.time = kwargs.get('time', 0)
        self.alt = kwargs.get('alt', 0)
        self.vel = kwargs.get('vel', 0)
    
    def update(self, **kwargs):
        self.__dict__.update(kwargs)
    
    def output(self, filename='output.json', stream=None):
        if stream:
            json.dump(self.__dict__, stream, separators=(',', ':'))
        else:
            with open(filename, 'w') as output_file:
                json.dump(self.__dict__, output_file, separators=(',', ':'))

logger.debug('State Module Loaded')