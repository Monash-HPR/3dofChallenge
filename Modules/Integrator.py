import numpy as np
from Modules.Forces import Propulsion
from Modules.Forces import Aerodynamics
from Modules.Forces import Inertia
from Modules import Geodesy
from Modules import Transformations
from Modules import Structures

def eulerIntegration(State):
    # Determine the inertial acceleration
    State.aB_I_I = Structures.get_aB_I_I(State)

    # Integrate for the velocity using Eulers method
    State.vB_I_I = State.vB_I_I + State.aB_I_I * State.dt

    # Integrate for position using Eulers method

    State.sBI__I = State.sBI__I + State.vB_I_I * State.dt
    #print(State.vB_I_I,State.sBI__I)

    # Update other state variables
    # T_GI = Transformations.get_T_GI(State.lat,State.lon) #Not currently used
    State.aB_E_G = State.aB_I_I
    State.vB_E_G = State.vB_E_G + State.aB_E_G * State.dt
    State.sB_E_G = Geodesy.getGeocentricPosition(State)
    Structures.updateMass(State)
    State.time += State.dt
    return
