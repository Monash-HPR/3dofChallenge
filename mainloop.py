import modules.Transformation as Transformation
import modules.Integrator as Integrator
import modules.Objects as Objects
import modules.Atmosphere as Atmosphere
import numpy as np
import time


# Initialisation
print('Testing...')
# Test cases
print(Atmosphere.temp(0))
print(Atmosphere.temp(5000))
print(Atmosphere.pressure(0))
print(Atmosphere.pressure(5000))
print(Atmosphere.density(5000))
print(Transformation.T_GE(-37.8136, 144.9631))
print(Transformation.T_GE(-37.8136, 144.9631)[0][0])
print(Transformation.T_EI(90))
print(Transformation.T_VG([0.0001, 0.0005, 25]))
