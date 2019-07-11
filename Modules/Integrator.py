import numpy as np
from Modules.Forces import Propulsion
from Modules.Forces import Aerodynamics
from Modules.Forces import Inertia
from Modules import Transformations
from Modules import Structures

def eulerIntegration(State):
    # Determine the inertial acceleration
    State.aB_I_I = Structures.get_aB_I_I(State)

    # Integrate for the velocity using Eulers method
    State.vB_I_I = State.vB_I_I + State.aB_I_I * State.dt
    

    # Integrate for position using Eulers method

    State.sBI__I = State.sBI__I + State.vB_I_I * State.dt

    # Update other state variables
    T_DI = Transformations.get_T_DI(State.sBI__I,State.time)
    State.vB_E_D = State.vB_E_D + np.matmul(T_DI,State.aB_I_I * State.dt)
    State.aB_E_D = np.matmul(T_DI,State.aB_I_I)
    Structures.updateMass(State)
    State.time += State.dt
    return
