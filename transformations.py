# file for establishing transformations
# angles
def headingAngle(State):
    headingAngle = numpy.arctan(State.velocityG(1)/State.velocityG(0))
    return headingAngle

def flightPathAngle(State):
    flightPathAngle = numpy.arctan(-State.velocityG(2)/numpy.sqrt(State.velocityG(0)**2 + State.velocityG(1)**2))
    return flightPathAngle

# transformation matrix from velocity to geographical coords
def tVG(State):
    h = headingAngle(State)
    fp = flightPathAngle(State)

    # creating matrix
    d = 3
    tVG = [[0 for x in range(d)] for y in range(d)]

    # assigning values from Zipfel
    tVG[0][0] = numpy.cos(fp)*numpy.cos(h)
    tVG[1][0] = -numpy.sin(h)
    tVG[2][0] = numpy.sin(fp)*numpy.cos(h)
    tVG[0][1] = numpy.cos(fp)*numpy.sin(h)
    tVG[1][1] = numpy.cos(h)
    tVG[2][1] = numpy.sin(fp)*numpy.sin(h)
    tVG[0][2] = -numpy.sin(fp)
    tVG[1][2] = 0
    tVG[2][2] = numpy.cos(fp)

    return tVG

# transformation matrix from georgraphical to earth coords
def tGE(State):
    lat = State.lat
    long = State.long

    # creating matrix
    d = 3
    tGE = [[0 for x in range(d)] for y in range(d)]

    # assigning values from Zipfel
    tGE[0][0] = -numpy.sin(lat)*numpy.cos(long)
    tGE[1][0] = -numpy.sin(long)
    tGE[2][0] = -numpy.cos(lat)*numpy.cos(long)
    tGE[0][1] = -numpy.sin(lat)*numpy.sin(long)
    tGE[1][1] = numpy.cos(long)
    tGE[2][1] = -numpy.cos(lat)*numpy.sin(long)
    tGE[0][2] = numpy.cos(lat)
    tGE[1][2] = 0
    tGE[2][2] = -numpy.sin(lat)

    return tGE

def tVE(State):
    tVE = tVG(State)*tGE(State)
    return tVE
