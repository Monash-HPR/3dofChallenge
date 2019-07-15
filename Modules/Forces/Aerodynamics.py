import numpy as np
from Modules import Atmosphere
from Modules import Structures

def getDragCoefficient(State):
    # Calculates that drag coefficent at a given Mach number from an approximate analytical function
    M = Atmosphere.getMach(State)
    # return 2400 * (np.exp(-1.2 * M) * np.sin(M) + (M / 6) * np.log10(M + 1))
    return 0.45

def getAerodynamicForce(State):
    # Returns the aerodynamic force vector in Body
    # Returning the force in velocity coords is only acceptable in a 3DOF simulation without horizontal winds
    # NOTE This needs converting to velocity coordinates
    # Prior to apogee, the drag is the body drag. after apogee, the drag is the parachute forces
    if State.vB_E_G[0] >= 0:
        cD = getDragCoefficient(State)
        s = State.reference_area
        q = Atmosphere.getDynamicPressure(State)
        return q * s * np.array([ [-cD], [0.0], [0.0]])

    elif Structures.getAltitude(State) > State.main_deploy / 3.28084:
        cD = State.drogue_cD
        s = State.drogue_area
        q = Atmosphere.getDynamicPressure(State)
        return q * s * np.array([ [cD], [0.0], [0.0]])

    else:
        cD = State.parachute_cD
        s = State.parachute_area
        q = Atmosphere.getDynamicPressure(State)
        return q * s * np.array([ [cD], [0.0], [0.0]])
