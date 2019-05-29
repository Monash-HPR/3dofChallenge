import math
import numpy as np
from modules import transforms as tr

To = 288.15
g0 = 9.81
p0 = 101325
L = -0.0065
R = 287.16
GM = 3.986 * 10**14
Re = 6.378137 *10**6
gamma = 1.4



def drag(velocity, area, Cd, h):
    p = pressure(h)
    t = temp(h)
    d = 0.5 * density(p, t) * velocity**2 * area * Cd
    return d


def cd(v, h):
    M = mach(v, h)
    #self.cd = 2400 * (math.exp(-1.2*m) * math.sin(m) + (m / 6) * math.log(m + 1, 10))
    if M == 0:
        cd = 0
    else:
        Cd1 = (0.5*math.exp(-2*M)*math.cos(5.5*M)) + 0.1*M*math.log(M) + 0.5
        cd = (math.exp(-0.5*M)*Cd1) + 0.1*math.exp(M-5)
    return cd


def pressure(h):
    pres = p0 * ((temp(h)/To)**5.2559)
    return pres


def temp(h):
    t = To + L*h
    return t


def density(p, t):
    den = p/(R*t)
    return den


def gravity(h):
    r = Re + h
    g = GM/(r**2)
    return g


def mach(v, h):
    m = v/math.sqrt(gamma*R*temp(h))
    return m


def Thrust(time, burntime, thrust0):
    if time > burntime:
        thrust = 0
    else:
        thrust = thrust0 * (1 - (10 ** -5 * math.exp((math.log1p(10 ** 5) / burntime) * time)))
    return thrust


def mass(time,burntime,mass0,massfuel):
    if time > burntime:
        return mass0 - massfuel
    else:
        m_dot = massfuel/burntime
        m = mass0 - time*m_dot
        return m


def acceleration_function(time,  velocity_i, altitude, x, y, lat, long, state):
    thrust0 = state[0]
    burntime = state[1]
    area = state[2]
    massfuel = state[3]
    mass0 = state[4]
    w_ei = state[5]

    current_velocity = np.linalg.norm(velocity_i)
    velocityG = np.matmul(tr.get_T_gi(lat, long, w_ei, time), velocity_i)

    net_aero = Thrust(time, burntime, thrust0) - drag(current_velocity, area, cd(current_velocity, altitude), altitude)
    netf_v = np.array([[net_aero], [0], [0]])
    mat_one = np.matmul(np.transpose(tr.get_T_vg(x, y, time, velocityG)), netf_v)

    mat_two = np.dot(mass(time,burntime,mass0,massfuel), np.array([[0], [0], [gravity(altitude)]]))
    mat_one_two = np.add(mat_one, mat_two)

    m_dvdt_i = np.matmul(np.transpose(tr.get_T_gi(lat, long, w_ei, time)), mat_one_two)
    dvdt_i = np.dot(1 / mass(time,burntime,mass0,massfuel), m_dvdt_i)
    return dvdt_i


