import numpy as np
# calculating the acceleration due to gravity
def getGravity(State):
    # finding Earth's centrifugal acceleration
    def aCentrifugal(State):
        # from Zipfel
        wEarth = np.array([0, 0, 7.292115*(1e-5)])
        wEarth = np.transpose(wEarth)
        aCentrifugal = (wEarth**2)*State.h

        return aCentrifugal

    # finding gravitational acceleration
    def aGravitational(State):
        GM = 3.986005*(1e14)
        aGravitational = -GM/(State.h**2)

        return aGravitational

    # total acceleration due to gravity
    g = aGravitational - aCentrifugal

    return g

# calculating temperature at given altitude
def getTemp(State):
    temp = 288.15 - 0.0065*State.h
    return temp

# calculating pressure
def getPressure(State, temp):
    p = 101325*(temp/288.15)**5.2559
    return p

# finding density
def getDensity(State, p, temp):
    R = 8.314
    density = p/(R*temp)
    return density

# calculating dynamic pressure
def getDynamicPressure(State):
    temp = getTemp(State)
    p = getPressure(State, temp)
    density = getDensity(State, p, temp)
    
    q = (density/2)*State.vB_E**2
    return q

# calculating Mach number
def getMach(State):
    T = getTemp(State)
    gamma = 1.4
    R = 8.314
    M = State.vB_E/np.sqrt(gamma*R*T)
    return M
    