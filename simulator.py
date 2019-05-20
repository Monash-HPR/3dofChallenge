# importing modules for use in simulation
import numpy as np
import modules.rocket as Rocket
import modules.transformations as Transformations
import modules.integrator as Integrator

# initialisation
rocket = Rocket.RocketClass()
motor = Rocket.Motor()
# inputs for state class
vB_E = 0
X = 0
Y = 0
lat = -37
lon = 144
h = 0
state = Rocket.State(vB_E, X, Y, lat, lon, h)

# transforming into inertial coordinates
def getInertialDisplacement(State):
    sBI__E = Transformations.getT_EG(State)*State.sBI__G
    sBI__I = Transformations.getT_IE(State)*sBI__E
    return sBI__I

state.sBI__I[0] = getInertialDisplacement(state)

def getInertialVelocity(State):
    T_IG = Transformations.getT_IG(State)
    o__EI_I = np.array([0, 0, 7.292115*(1e-5)])
    o__EI_I = np.transpose(o__EI_I)
    
    vB_I_I = T_IG*State.vB_E_G + o__EI_I*State.sBI__I
    return vB_I_I

state.vB_I_I[0] = getInertialVelocity(state)

# main loop
# counter
c = 0
while c <= state.points:
    # updating variables for force calculations
    state.h = state.sBI__I[c][2]
    state.vB_E = state.vB_I_I[c][0]
    
    # set 'previous' values for integration
    sPrev = state.sBI__I[c]
    vPrev = state.vB_I_I[c]
    
    # updating time
    state.currentTime = state.time[c]
    
    # intergrator for velocity
    v = Integrator.getVelocity(state, vPrev, motor, rocket)
    
    # displacement
    s = Integrator.getDisplacement(sPrev, v)
    
    # updating State class
    state.vB_I_I[c+1] = v
    state.sBI__I[c+1] = s
    
    # updating counter
    c = c + 1
    
# transforming variables back to geographical coords for convenience
def getDisplacements(State):
    T_EI = Transformations.getT_EI(State)
    sBI__E = T_EI*State.sBI__I
    return sBI__E

sBI__E = getDisplacements(state)
lat_array = sBI__E[0]
lon_array = sBI__E[1]
h_array = sBI__E[2]

def getVelocitys(State):
    o__EI_I = np.array([0, 0, 7.292115*(1e-5)])
    o__EI_I = np.transpose(o__EI_I)
    T_GI = Transformations.getT_GI(State)
    
    vB_E_G = T_GI*(State.vB_I_I - o__EI_I*State.sBI__I)
    return vB_E_G

state.vB_E_G = getVelocitys(state)
vB_E_array = state.vB_E_G[0]
X_array = state.vB_E_G[1]
Y_array = state.vB_E_G[2]
    