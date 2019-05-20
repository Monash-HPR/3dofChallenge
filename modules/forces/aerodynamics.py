import geophysics as geo
import numpy as np

# calculating the drag coefficient
def getDragCoefficient(State):
    M = geo.getMach(State)
    
    C_D = 2400*(np.exp(-1.2*M)*np.sin(M) + (M/6)*np.log10(M+1))
    
    return C_D

# how do you get Cl????
def getLiftCoefficient(State):
    C_D = getDragCoefficient(State)
    
    # making up formulas here... sort of based on 8.19
    C_L = np.sqrt(C_D)
    return C_L
