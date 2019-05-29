import numpy as np

def get_T_vg(x, y, time, velocityG):  # need to fix this function
    # heading angle
    if time > 0.03:
        temp1 = velocityG[0][0]
        if temp1 == 0:
            x = 0
        else:
            x = np.arctan(velocityG[1][0] / velocityG[0][0])

        # flight path angle
        temp2 = np.sqrt(velocityG[0][0] ** 2 + velocityG[1][0] ** 2)
        if temp2 == 0:
            y = np.pi / 2
        else:
            y = np.arctan(-velocityG[2][0] / temp2)

    sx = np.sin(x)
    if sx < 1e-10:
        sx = 0
    cx = np.cos(x)
    if cx < 1e-10:
        cx = 0
    sy = np.sin(y)
    if sy < 1e-10:
        sy = 0
    cy = np.cos(y)
    if cy < 1e-10:
        cy = 0

    T_vg = np.array([[cy * cx, cy * sx, -1 * sy], [-sx, cx, 0], [sy * cx, sy * sx, cy]])
    return T_vg


def get_T_ge(lat, long):
    slong = np.sin(long)
    clong = np.cos(long)
    slat = np.sin(lat)
    clat = np.cos(lat)

    T_ge = np.array([[-slat*clong, -slat*slong, clong], [-slong, clong, 0], [-clat*clong, -clat*slong, -slat]])
    return T_ge


def get_T_ei(w_ei, time):
    hour_angle = w_ei * time
    ch = np.cos(hour_angle)
    sh = np.sin(hour_angle)

    t_ei = np.array([[ch, sh, 0], [-sh, ch, 0], [0, 0, 1]])
    return t_ei


def get_T_gi(lat, long, w_ei, time):
    T_ge = get_T_ge(lat, long)

    T_ei = get_T_ei(w_ei, time)
    T_gi = np.matmul(T_ge, T_ei)
    return T_gi