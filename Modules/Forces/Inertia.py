import numpy as np
from Modules import Geodesy
from Modules import Transformations

def getGravityAcceleration(State):
    # Calculate gravitation acccleration
    g = get_g__G(State.sBI__I)

    # Calculate centrifugal force due to Earth's Rotation
    wEI__I = Geodesy.get_WBE__I()
    omegaEI__I =Transformations.skewSymmetricExpansion(wEI__I)
    f = np.matmul(np.matmul(omegaEI__I,omegaEI__I),State.sBI__I)

    return g-f
