import numpy as np
from Modules import Atmosphere

def getDragCoefficient(State):
    M = Atmosphere.getMach(State)
    return 2400 * (np.exp(-1.2 * M) * np.sin(M) + (M / 6) * np.log10(M + 1))
