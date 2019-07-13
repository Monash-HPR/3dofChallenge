import numpy as np
from Modules import Geodesy
from Modules import Transformations

def getGravityAcceleration(State):
    # Calculate gravitation acccleration
    g = Geodesy.get_g__G(State)

    # Calculate centrifugal force due to Earth's Rotation
    omegaEI__I = Geodesy.get_omegaEI__I()
    f = np.matmul(np.matmul(omegaEI__I,omegaEI__I),State.sBI__I)
    return g
