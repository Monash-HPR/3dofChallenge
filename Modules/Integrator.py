import numpy as np
from Modules.Forces import Propulsion
from Modules.Forces import Aerodynamics
from Modules.Forces import Inertia
from Modules import Structures

def eulerIntegration(State):
    # Determine the inertial acceleration
    aB_I_I = Structures.get_aB_I_I(State)

    # Integrate for the velocity using Eulers method
    State.vB_I_I = State.vB_I_I + aB_I_I * State.dt

    # Integrate for position using Eulers method

    State.sBI__I = State.sBI__I + State.vB_I_I * State.dt

    # Update other state variables
    State.vB_E_D = Structures.get_vB_E_D(State)
    State.time += State.dt
    return
