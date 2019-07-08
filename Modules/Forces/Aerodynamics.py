import numpy as np
from Modules import Atmosphere

def getDragCoefficient(State):
    # Calculates that drag coefficent at a given Mach number from an approximate analytical function
    M = Atmosphere.getMach(State)
    return 2400 * (np.exp(-1.2 * M) * np.sin(M) + (M / 6) * np.log10(M + 1))
