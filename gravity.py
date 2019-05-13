# calculating the acceleration due to gravity
def gravity(State):
    # finding Earth's centrifugal acceleration
    def aCentrifugal(State):
        # from Zipfel
        wEarth = [0; 0; 7.292115*(10**-5)]
        aCentrifugal = (wEarth**2)*State.height

        return aCentrifugal

    # finding gravitational acceleration
    def aGravitational(State):
        # from Zipfel
        GM = 3.986005*(10**14)
        aGravitational = -GM/(State.height**2)

        return aGravitational

    # total acceleration due to gravity
    g = aGravitational - aCentrifugal

    return g

# force due to gravity
def gravityForce(State, Rocket):
    g = gravity(State)

    gravityForce = g*Rocket.getMass

    return gravityForce
