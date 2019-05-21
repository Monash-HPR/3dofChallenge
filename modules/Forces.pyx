import numpy as np
from modules import Atmosphere

r0 = 6356766.0
def dragForce(rocketState, rocketParams):
  pos = rocketState.position
  vel = rocketState.velocity
  altitude = pos[2]-r0
  a = Atmosphere.speedsound(altitude)
  rho = Atmosphere.density(altitude)
  M = np.linalg.norm(vel)/a
  q = 0.5*rho*vel
  area = 0.25*np.power(rocketParams.diameter,2)
  cd = 2400 * (np.exp(-1.2*M) * np.sin(M) + (M/6) * np.log10(M+1))
  drag_f = -q*area*cd
  return drag_f

def grav(rocketState):
  GM = 3.986*np.power(10, 14)
  g0 = -GM/(rocketState.position[2])
  omega2 = np.power(7.292115*np.power(10.0, -5), 2)
  g_f = [0, 0, g0 + omega2*(rocketState.position[2])]
  return g_f

def thrustForce(rocketState, rocketParams):
  if rocketState.time <= rocketParams.burnout_time:
    thrust = rocketParams.avgthrust
    return np.array([thrust, 0,0])
  else:
    return np.array([0,0,0])

def spForce(rocketState, rocketParams):
  bank_angle = 0
  aoa = 0 # for now
  T = thrustForce(rocketState, rocketParams)
  D = dragForce(rocketState, rocketParams)
  f1 = T[0]*np.cos(aoa) + D[0]
  f2 = np.sin(bank_angle)*(T[1]*np.sin(aoa))
  f3 = -np.cos(bank_angle)*(T[2]*np.sin(aoa))
  force = np.array([f1, f2, f3])*(1/rocketParams.mass)
  return force
