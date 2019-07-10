import numpy as np
from Modules import Geodesy
from Modules import Transformations

def getGravityForce(State):
    # Calculate gravitation acccleration
    g = get_g__G(State.sBI__I)

    # Calculate centrifugal force due to Earth's Rotation
    # wEI__I = Geodesy.get_WBE__I()
    # omegaEI__I
    # FIX THIS LATER

    return g
