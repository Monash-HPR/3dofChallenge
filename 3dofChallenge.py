import math
import numpy as np

class Rocket:
    def __init__(self,inital_altitude=0):
        self.mass = 35 #subject to change
        self.motorCaseMass = 1 #subject to change
        self.massFuel = 2
        self.pressure0 = 101325
        self.temperature0 = 288.15
        self.g0 = 9.81
        self.R = 287.16
        self.L = -0.0065
        self.GM = 3.986 * 10**14
        self.Re = 6378137
        self.Sei = [[self.Re], [0], [0]]
        self.rocket_area = math.pi * (0.127/2)**2 #subject to change
        self.time = [0] #will be turned into a list
        self.timestep = 0.01 #subject to change
        self.thrust0 = 5800 #guess again
        self.burntime = 3.5 #guess again
        self.g = [0,0,0]
        self.lat = 0
        self.long = 0
        self.w_ei = 2*np.pi/(24*60*60)
        self.w_ei_e = [[0, self.w_ei, 0], [self.w_ei, 0, 0], [0, 0, 0]]
        self.T_vg = []

        self.dragB = 0
        self.density = 0
        self.pressure = 101325
        self.temperature = 288.15
        self.velocityB = [[0], [0], [0]]
        self.velocityG = [[0],[0],[0]]
        self.Sbe = [[inital_altitude], [0], [0]]
        self.Sbi = np.add(self.Sbe, self.Sei)
        self.cd = 0
        self.mach = 0
        self.thrust = 0
        self.y = np.pi/3
        self.x = 0
        self.Acc_mat = []

    def get_altitude(self):
        #self.Sbe = np.add(self.Sbi, np.dot(-1, self.Sei))

        return self.Sbe[0][0]

    def get_drag(self):
        self.dragB = 0.5*self.get_density()*(self.velocityB[-1][0]**2)*self.rocket_area*self.get_cd()
        return self.dragB

    def get_temperature(self):
        self.temperature = self.temperature0 + self.L*self.get_altitude()
        return self.temperature

    def get_pressure(self):
        self.pressure = self.pressure0*((self.get_temperature()/self.temperature0)**(self.g0*self.L))
        return self.pressure

    def get_density(self):
        self.density = self.get_pressure()/(self.R*self.get_temperature())
        return self.density

    def get_cd(self):
        m = self.get_mach()
        self.cd = 2400 * (math.exp(-1.2*m) * math.sin(m) + (m / 6) * math.log(m + 1, 10))
        return self.cd

    def get_mach(self):
        self.mach = abs(self.velocityB[0][0]/(1.4*self.R*self.get_temperature())**0.5)
        return self.mach

    def get_thrust(self):
        if self.time[-1] > self.burntime:
            self.thurst = 0
        else:
            self.thrust = self.thrust0 * (1 - (10 ** -5 * math.exp((math.log1p(10 ** 5) / self.burntime) * self.time[-1])))
        return self.thrust

    def get_gravity(self):
        r = self.Re + self.get_altitude()
        grav = self.GM/r
        grav = grav/r
        self.g = [[0], [0], [grav]]
        return self.g

    def get_mass(self): #not finishind this function at all just ill do it later
        return self.mass

#backed ^^

    def get_T_vg(self):

        '''       
        #heading angle
        temp1 = self.velocityG[-1][0]
        if temp1 == 0:
            x = 0
        else:
            x = np.arctan(self.velocityG[-1][1] / self.velocityG[-1][0])

        #flight path angle
        temp2 = math.sqrt(self.velocityG[-1][0]**2 + self.velocityG[-1][1]**2)
        if temp2 == 0:
           y = np.pi/2
        else:
           y = np.arctan(self.velocityG[-1][2]/temp2)
        '''


        sx = np.sin(self.x)
        if sx < 10**-10:
            sx = 0
        cx = np.cos(self.x)
        if cx < 10**-10:
            cx = 0
        sy = np.sin(self.y)
        if sy < 10**-10:
            sy = 0
        cy = np.cos(self.y)
        if cy < 10**-10:
            cy = 0

        self.T_vg = [[cy*cx, cy*sx, -1*sy],[-sx, cx, 0],[sy*cx, sy*sx, cy]]
        return self.T_vg


    def get_T_ge(self):
        slong = math.sin(self.long)
        clong = math.cos(self.long)
        slat = math.sin(self.lat)
        clat = math.cos(self.lat)

        T_ge =  [[-slat*clong, -slat*slong, clong],[-slong, clong, 0],[-clat*clong, -clat*slong, -slat]]
        return T_ge

    def get_T_ve(self):
        T_vg = self.get_T_vg()
        T_ge = self.get_T_ge()
        T_ve = np.matmul(T_vg,T_ge)
        return T_ve


    def get_netF_aero_prop(self):
        self.netF_aero_propB = self.get_thrust() - self.get_drag()
        return self.netF_aero_propB

    def integrator_step(self):
        netF_aero_propV = [[self.get_netF_aero_prop()], [0], [0]]
        f_on_m = np.dot(netF_aero_propV, 1/self.get_mass())
        g_v = np.matmul(self.get_T_vg(), self.get_gravity())
        mat_one = np.add(f_on_m,g_v)

        T_ve = self.get_T_ve()
        mat_two = np.matmul(T_ve, self.w_ei_e)
        mat_two = np.matmul(mat_two, np.transpose(T_ve))
        mat_two = np.matmul(mat_two, self.velocityB)
        mat_two = np.dot(-2, mat_two)
        print(mat_two)

        mat_three = np.matmul(self.get_T_ve(), self.w_ei_e)
        mat_three = np.matmul(mat_three, self.w_ei_e)
        mat_three = np.matmul(mat_three, self.Sbi)
        mat_three = np.dot(-1, mat_three)


        dvdt = np.add(mat_one, mat_two)
        self.Acc_mat = np.add(dvdt, mat_three)

        v_dot = self.Acc_mat[0][0]
        print('.',v_dot)
        v_new = [[self.velocityB[0][0] + v_dot*self.timestep], [0], [0]]
        v_old = self.velocityB
        self.velocityB = v_new


        s_dot = np.matmul(np.transpose(self.get_T_ve()), v_old)

        self.Sbe = np.add(self.Sbe, np.dot(s_dot, self.timestep))

        self.Sbi = np.add(self.Sbe,self.Sbi)

        #now know v can solve for y_dot
        y_dot = (self.Acc_mat[2]/-v_new[0][0])[0]
        self.y = self.y + y_dot*self.timestep


        #now know y can compute x_dot
        x_dot = (self.Acc_mat[1]/(np.cos(self.y)*v_new[0][0]))[0]
        self.x = self.x + x_dot*self.timestep

        self.time.append(self.time[-1] +self.timestep)
        return v_new[0][0]

    def integrator(self):
        v = self.integrator_step()
        alt = self.get_altitude()
        for i in range(1):
            v = self.integrator_step()
            print(self.Sbi,self.y)
        return self.get_altitude()

rock = Rocket(0)
print(rock.integrator())
print(max(rock.time))