import numpy as np

# creating a class to hold the rocket's properties
class RocketClass():
    def __init__(self):
        # data from induction challenge
        self.radius = 0.127/2
        self.area = (self.radius**2)*np.pi
        self.bodyMass = 26

    # updating total mass as fuel burns
    @property
    def getMass(self, Motor):
        self.mass = self.bodyMass + Motor.getMass
        return self.mass

# class containing motor data
class Motor():
    def __init__(self):
        # data from induction challenge
        self.fuelMass = 8
        self.motorCasing = 1
        self.peakThrust = 5800
        self.tBurnout = 3.5

    # updating the fuel mass as the motor burns
    @property
    def getMass(self, State):
        if State.currentTime <= self.tBurnout:
            self.mass = self.fuelMass - (self.fuelMass/self.tBurnout)*State.currentTime + self.motorCasing
        else:
            self.mass = self.motorCasing
        return self.mass

# state class to describe the rocket's motion over time
class State(vB_E, X, Y, lat, lon, h):
    def __init__(self, vB_E, X, Y, lat, lon, h):
        self.vB_E = vB_E
        self.X = X
        self.Y = X
        self.lat = lat
        self.lon = lon
        self.h = h
        self.maxTime = 60
        self.currentTime = 0
        self.dt = 0.01
        self.time = np.arrange(0, self.maxTime, self.dt)
        self.points = np.size(self.time)
        self.vB_E_G = np.zeros(3, self.points)
        self.vB_E_G[0][0] = self.vB_E
        self.vB_E_G[0][1] = self.X
        self.vB_E_G[0][2] = self.Y
        self.vB_I_I = np.zeros(3, self.points)
        self.sBI__G = np.zeros(3, self.points)
        self.sBI__G[0][0] = 0
        self.sBI__G[0][1] = 0
        # radius of the earth
        self.sBI__G[0][2] = -(6371000 + h)
        self.sBI__I = np.zeros(3, self.points)
