import numpy as np
from Modules import Atmosphere

def getDragCoefficient(State):
    # Calculates that drag coefficent at a given Mach number from an approximate analytical function
    M = Atmosphere.getMach(State)
    #return 2400 * (np.exp(-1.2 * M) * np.sin(M) + (M / 6) * np.log10(M + 1)) # NEEDS FIXING
    return 0.5

def getAerodynamicForce(State):
    # Returns the aerodynamic force vector in velocity coordinates
    # Returning the force in velocity coords is only acceptable in a 3DOF simulation without horizontal winds
    cD = getDragCoefficient(State)
    s = State.reference_area
    q = Atmosphere.getDynamicPressure(State)
    return q * s * np.array([ [-cD], [0.0], [0.0]])
