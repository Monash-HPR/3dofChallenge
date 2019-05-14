import json
import logging
import numpy as np

logger = logging.getLogger(__name__)

class State:
    def __init__(self, **kwargs):
        logger.debug('Creating State Instance')
        self.time = kwargs.get('time', np.array([0.0, 0.0, 0.0], np.float64))
        self.alt = kwargs.get('alt', np.array([0.0, 0.0, 0.0], np.float64))
        self.vel = kwargs.get('vel', np.array([0.0, 0.0, 0.0], np.float64))
        self.acc = kwargs.get('acc', np.array([0.0, 0.0, 0.0], np.float64))
        self.mass = kwargs.get('mass', np.array([0.0, 0.0, 0.0], np.float64))
        self.drag = kwargs.get('drag', np.array([0.0, 0.0, 0.0], np.float64))
        self.gravity = kwargs.get('gravity', np.array([0.0, 0.0, 0.0], np.float64))
    
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