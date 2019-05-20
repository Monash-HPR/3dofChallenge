# assuming a linear model for thrust
def getThrust(State, Motor):
    
    if State.currentTime <= Motor.tBurnout:
        F = Motor.peakThrust/Motor.tBurnout
    else:
        F = 0
        
    return F
