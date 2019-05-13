# creating a class to hold the rocket's properties
class Rocket():
    def __init__(self):
        # data from induction challenge
        self.radius = 0.127/2
        self.area = (self.radius**2)*numpy.pi
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
class State():
    def __init__(self):
        self.currentTime = 0
        self.time = []
        self.displacement = [0; 0; 0]
        self.velocityG = [0; 0; 0]
        self.velocityV = [0; 0; 0]
        self.speed = []
        self.headingRate = []
        self.flightPathRate = []
        # random values based on my phone's location
        self.lat = -37
        self.long = 145
