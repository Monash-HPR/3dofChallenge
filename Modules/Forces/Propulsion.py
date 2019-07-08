import numpy as np

def getThrust(State):
    if State.time < State.burn_time:
        return State.thrust
    else
        return 0.0
    
