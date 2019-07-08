import numpy as np
from Modules import Structures

def getTemperature(State):
    # Returns atmospheric temperature as specified by ISA 1976
    h = Structures.getAltitude(State)
    if h < 11000:
        return 288.15 - 0.0065*h
    else
        return 216

def getPressure(State):
    # Returns the atmospheric pressure as specified by ISA 1976
    h = Structures.getAltitude(State)
    if h < 11000:
        T = getTemperature(State)
        return 101325 * (T/288.15)**5.2559
    else
        return 22630 * np.exp(-0.00015769 * (h - 11000))

def getDensity(State):
    # Uses the ideal gas law to retrieve density from the other ISA models
    p = getPressure(State)
    T = getTemperature(State)
    R = 287.058                     #Specific Gas constant of dry air
    return p/(R*T)

def getSonicSpeed(State):
    gamma = 1.4             # Ratio of specific heats for air
    R = 287.058             #Specific Gas constant of dry acquire
    T = getTemperature(State)
    return np.sqrt(gamma * R * T)

def getDynamicPressure(State):
    V = np.linalg.norm(State.vB_I_I)
    density = getDensity(State)
    return 0.5 * density * V**2

def getMach(State):
    V = np.linalg.norm(State.vB_I_I)
    a = getSonicSpeed(State)
    return V/a
