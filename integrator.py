# file for integrating functions
# finding change in velocity
def getVelocity(State, Rocket):
    # need to find total force
    def totalForce(State, Rocket):
        fG = gravityForce(State, Rocket)
        fD = 0 ## implement later, remember to check sign
        fT = 0 ## implement later

        totalForce = fG + fD + fT
        return totalForce

    def getDerivative(State, Rocket):
        # Earth's angular velocity wrt Earth
        wEarth = [0; 0; 7.292115*(10**-5)]

        tVE = tVE(State)

        # evaluating each term individually first for simplicity
        t1 = totalForce(State, Rocket)/Rocket.getMass
        t2 = tVG(State)*gravity(State)
        t3 = 2*tVE*wEarth*numpy.transpose(tVE)*State.velocityV
        t4 = tVE*wEarth*wEarth*State.displacement

        derivative = t1 + t2 - t3 - t4

        # adjusting so matrix corresponds to derivative of each component
        fp = flightPathAngle(State)
        v = State.velocityV[0]
        derivative[1] = derivative[1]/(v * numpy.cos(fp))
        derivative[2] = -derivative[2]/v

        return derivative

    dt = 0.001

    # implementing Euler's method - will look at using more accurate one later
    vMatrix = State.velocityG + dt*getDerivative(State, Rocket)

    # updating state
    State.speed.append(vMatrix[0])
    State.headingRate.append(vMatrix[1])
    State.flightPathRate.append(vMatrix[2])

    State.velocityG = vMatrix

    # calculating total velocity
    vTotal = numpy.linalg.norm(vMatrix)

    State.velocityV[0] = vTotal

    return vTotal

# finding change in displacement
def getDisplacement(State):
    derivative = numpy.transpose(tVE(State))*State.velocityV

    # again, using Euler's method for the time being
    dt = 0.001
    newDisplacement = State.displacement + dt*derivative
    State.displacement.append(newDisplacement)

    return newDisplacement
    
