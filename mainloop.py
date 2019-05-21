import modules.Transformation as Transformation
import modules.Integrator as Integrator
import modules.Objects as Objects
import modules.Atmosphere as Atmosphere
import modules.Forces as Forces
import numpy as np
import time


# Initialisation
print('Testing...')
r0 = 6356766.0
pos_g = np.array([-37.8136, 144.9631, 0+r0])
poszero_g = np.array([-37.8136, 144.9631, 0+r0])
# Test cases
print(Atmosphere.temp(0))
print(Atmosphere.temp(5000))
print(Atmosphere.pressure(0))
print(Atmosphere.pressure(5000))
print(Atmosphere.density(5000))
print(Transformation.T_GE(pos_g))
print(Transformation.T_GE(poszero_g))
print(Transformation.T_GE(pos_g)[0][0])
print(Transformation.T_EI(90))
print(Transformation.T_VG(np.array([0, 0, 25])))
print(Transformation.T_VG(np.array([0.0001, 0.0005, 25])))
print(np.transpose(Transformation.T_GE(pos_g)))

print("Object testing...")
position = np.array([-37.8136, 144.9631, 0+r0])
velocity = np.array([0.001, 0, 15])
history =[]
time = 0
v_g = np.matmul(Transformation.T_GI(position, time), velocity)
print(v_g)
rocket = Objects.rocketState(position, velocity, history, time)
print(Transformation.T_VG(rocket.velocity))
print(Transformation.T_GE(rocket.position))
print(rocket)
properties = Objects.rocketParams(0.4, 0)
print(properties)

print("Forces testing...")
print(Forces.spForce(rocket, properties))
rocket.updateTime(4)
properties.updateTime(4)
print(Forces.spForce(rocket, properties))
rocket.updateTime(12)
properties.updateTime(12)
print("Time = 12")
print(rocket, properties)
print(Forces.spForce(rocket, properties))
check = np.matmul(np.transpose(Transformation.T_GI(rocket.position, 12)), np.transpose(Transformation.T_VG(rocket.velocity)))
