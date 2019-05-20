# calculating specific force
import numpy as np
import aerodynamics as aero
import propulsion as propulsion
import geophysics as geo

def getSpecificForce(State, Motor, Rocket):
    # getting aero forces
    C_D = aero.getDragCoefficient(State)
    C_L = aero.getLiftCoefficient(State)
    
    # getting propulsion force
    F = propulsion.getThrust(State, Motor)
    
    # dynamic pressure
    q = geo.getDynamicPressure(State)
    
    # angle of attack and bank angle????
    alpha = 0
    phi = 0
    
    # surface area of rocket
    S = Rocket.area
    
    # assigning values to matrix
    fap0 = F*np.cos(alpha) - q*S*C_D
    fap1 = np.sin(phi)*(F*np.sin(alpha) + q*S*C_L)
    fap2 = -np.cos(phi)*(F*np.sin(alpha) + q*S*C_L)
    
    # creating matrix
    fap = np.array([[fap0], [fap1], [fap2]])
    
    # specific force
    fsp__V = (1/Rocket.mass)*fap
    
    return fsp__V
