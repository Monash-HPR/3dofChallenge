# file for establishing transformations
import numpy as np

# initial transformations
# transformation matrix from georgraphical to earth coords
def getT_GE(State):
    lat = State.lat
    lon = State.lon

    # assigning values from Zipfel
    T_GE_0 = [-np.sin(lat)*np.cos(lon), -np.sin(lat)*np.sin(lon), np.cos(lat)]
    T_GE_1 = [-np.sin(lon), np.cos(lon), 0]
    T_GE_2 = [-np.cos(lat)*np.cos(lon), -np.cos(lat)*np.sin(lon), -np.sin(lat)]
    
    # creating matrix    
    T_GE = np.array([[T_GE_0], [T_GE_1], [T_GE_2]])

    return T_GE

def getT_EG(State):
    T_GE = getT_GE(State)
    T_EG = np.transpose(T_GE)
    return T_EG

# transformation from earth to inertial
def getT_EI(State):
    # hour angle
    hA= np.pi/12
    T_EI = np.array([[np.cos(hA), np.sin(hA), 0], [-np.sin(hA), np.cos(hA), 0], [0, 0, 1]])
    return T_EI

# inertial to earth
def getT_IE(State):
    T_EI = getT_EI(State)
    T_IE = np.transpose(T_EI)
    return T_IE

# transformation from inertial to geographical
def getT_IG(State):
    T_IE = getT_IE(State)
    T_EG = getT_EG(State)
    T_IG = T_IE*T_EG
    return T_IG

def getT_GI(State):
    T_IG = getT_IG(State)
    T_GI = np.transpose(T_IG)
    return T_GI

# transformation matrix from velocity to geographical coords
def getT_VG(State):
    Y = State.Y
    X = State.X
    
    # assigning values from Zipfel
    T_VG_0 = [np.cos(Y)*np.cos(X), np.cos(Y)*np.sin(X), -np.sin(Y)]
    T_VG_1 = [-np.sin(X), np.cos(Y)*np.sin(X), 0]
    T_VG_2 = [np.sin(Y)*np.cos(X), np.sin(Y)*np.sin(X), np.cos(Y)]
    
    # creating matrix
    T_VG = np.array([[T_VG_0], [T_VG_1], [T_VG_2]])
    
    return T_VG

def getT_GV(State):
    T_VG = getT_VG(State)
    T_GV = np.transpose(T_VG)
    return T_GV
