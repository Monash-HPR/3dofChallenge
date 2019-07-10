import numpy as np

def getThrust(State):
    # Returns the thrust of the motor in body coordinates for a given time.
    if State.time < State.burn_time:
        return np.array([ [State.thrust], [0.0], [0.0]])
    else:
        return np.array([[0.0],[0.0],[0.0]])
