import json
import logging

logger = logging.getLogger(__name__)

class State:
    def __init__(self, **kwargs):
        logger.debug('Creating State Instance')
        self.time = kwargs.get('time', 0.0)
        self.alt = kwargs.get('alt', 0.0)
        self.vel = kwargs.get('vel', 0.0)
        self.acc = kwargs.get('acc', 0.0)
        self.mass = kwargs.get('mass', 0.0)
        self.drag = kwargs.get('drag', 0.0)
        self.gravity = kwargs.get('gravity', 0.0)
    
    def update(self, **kwargs):
        self.__dict__.update(kwargs)
        return self
    
    def copy(self):
        return State(**self.__dict__)
    
    def update_from(self, other_state):
        self.update(**other_state.__dict__)

    def update_to(self, other_state):
        other_state.update(**self.__dict__)

    def output(self, filename='output.json', stream=None):
        if stream:
            json.dump(self.__dict__, stream, separators=(',', ':'))
        else:
            with open(filename, 'w') as output_file:
                json.dump(self.__dict__, output_file, separators=(',', ':'))

logger.debug('State Module Loaded')