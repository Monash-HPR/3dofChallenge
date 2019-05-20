# file for integrating functions
import transformations as TMs
import forces.gravity as gravity
import forces.specifc_force as forces

# finding change in velocity
def getVelocity(State, vPrev, Motor, Rocket):
        
    # finding the derivative
    def getDerivative(State):
        T_IG = TMs.getT_IG(State)
        T_GV = TMs.getT_GV(State)
        fsp__V =  forces.getSpecificForce(State, Motor, Rocket)
        g = gravity.getGravity(State)
        
        derivative = T_IG*(T_GV*fsp__V + g)

        return derivative

    # implementing Euler's method - will look at using more accurate one later
    dv_dt = getDerivative(State)
    v = vPrev + vPrev*dv_dt

    return v

# finding change in displacement
def getDisplacement(sPrev, v):
    ds_dt = v
    
    # again, using Euler's method for the time being
    s = sPrev + sPrev*ds_dt

    return s
