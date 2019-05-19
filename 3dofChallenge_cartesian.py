import math
import numpy as np

class Rocket:
    def __init__(self,inital_altitude=0):
        self.mass0 = 35 #subject to change
        self.mass = 35
        self.motorCaseMass = 1 #subject to change
        self.massFuel = 9
        self.pressure0 = 101325
        self.temperature0 = 288.15
        self.g0 = 9.81
        self.R = 287.16
        self.L = 0.0065
        self.GM = 3.986 * 10**14
        self.Re = 6378137
        self.Sei = np.array([[0], [0], [0]])
        self.rocket_area = math.pi * (0.127/2)**2 #subject to change
        self.time = [0] #will be turned into a list
        self.timestep = 0.01 #subject to change
        self.thrust0 = 5800 #guess again
        self.burntime = 3.5 #guess again
        self.g = [0,0,0]
        self.lat = 0
        self.long = 0
        self.w_ei = 2*np.pi/(24*60*60)
        self.w_ei_e = np.array([[0, self.w_ei, 0], [self.w_ei, 0, 0], [0, 0, 0]])
        self.T_vg = []

        self.dragB = 0
        self.density = 0
        self.pressure = 101325
        self.temperature = 288.15
        self.velocityB = np.array([[0], [0], [0]])
        self.vb_i_i = np.array([[0],[0],[0]])
        self.Sbe = np.array([[inital_altitude+self.Re], [0], [0]])
        self.Sbi = np.add(self.Sbe, self.Sei)
        self.cd = 0
        self.mach = 0
        self.thrust = 0
        self.y = np.pi/2
        self.x = 0
        self.Acc_mat = []
        self.hour_angle = 0
        self.thrust = 0

    def get_altitude(self):
        #self.Sbe = np.add(self.Sbi, np.dot(-1, self.Sei))
        alt = self.Sbi[0][0] - self.Re
        return alt

    def get_drag(self):
        self.dragB = 0.5*self.get_density()*(np.linalg.norm(self.vb_i_i)**2)*self.rocket_area*self.get_cd()
        #print(self.dragB)
        return self.dragB

    def get_temperature(self):
        self.temperature = self.temperature0 - (self.L*self.get_altitude())
        return self.temperature

    def get_pressure(self):
        self.pressure = self.pressure0*((self.get_temperature()/self.temperature0)**(5.2559))
        return self.pressure

    def get_density(self):
        self.density = self.get_pressure()/(self.R*self.get_temperature())
        return self.density

    def get_cd(self):
        M = self.get_mach()
        #self.cd = 2400 * (math.exp(-1.2*m) * math.sin(m) + (m / 6) * math.log(m + 1, 10))
        if M == 0:
            self.cd = 0
        else:
            Cd1 = (0.5*math.exp(-2*M)*math.cos(5.5*M)) + 0.1*M*math.log(M) + 0.5
            self.cd = (math.exp(-0.5*M)*Cd1) + 0.1*math.exp(M-5)
        return self.cd

    def get_mach(self):
        self.mach = abs(np.linalg.norm(self.vb_i_i)/((1.4*self.R*self.get_temperature())**0.5))
        return self.mach

    def get_thrust(self):
        if self.time[-1] > self.burntime:
            self.thrust = 0
        else:
            self.thrust = self.thrust0 * (1 - ((10 ** -5) * math.exp((math.log1p(10 ** 5) / self.burntime) * self.time[-1])))
        #print(self.thrust)
        return self.thrust

    def get_gravity(self):
        r = self.Re + self.get_altitude()
        grav = self.GM/r
        grav = grav/r
        self.g = np.array([[0], [0], [grav]])
        return self.g

    def get_mass(self): #not finishind this function at all just ill do it later
        if self.time[-1] > self.burntime:
            return self.mass
        else:
            m_dot = self.massFuel/self.burntime
            self.mass = self.mass0 - self.time[-1]*m_dot
            return self.mass

#backend^^

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
        if sx < 1e-10:
            sx = 0
        cx = np.cos(self.x)
        if cx < 1e-10:
            cx = 0
        sy = np.sin(self.y)
        if sy < 1e-10:
            sy = 0
        cy = np.cos(self.y)
        if cy < 1e-10:
            cy = 0

        self.T_vg = np.array([[cy*cx, cy*sx, -1*sy],[-sx, cx, 0],[sy*cx, sy*sx, cy]])
        return self.T_vg

    def get_netF_aero_prop(self):
        self.netF_aero_propB = self.get_thrust() - self.get_drag()
        return self.netF_aero_propB

    def get_T_ge(self):
        slong = math.sin(self.long)
        clong = math.cos(self.long)
        slat = math.sin(self.lat)
        clat = math.cos(self.lat)

        T_ge = np.array([[-slat*clong, -slat*slong, clong], [-slong, clong, 0], [-clat*clong, -clat*slong, -slat]])
        return T_ge

    def get_T_ei(self):
        self.hour_angle = self.w_ei * self.time[-1]
        ch = np.cos(self.hour_angle)
        sh = np.sin(self.hour_angle)

        t_ei = np.array([[ch, sh, 0], [-sh, ch, 0], [0, 0, 1]])
        return t_ei

    def get_T_gi(self):
        T_ge = self.get_T_ge()

        T_ei = self.get_T_ei()
        T_gi = np.matmul(T_ge, T_ei)
        return T_gi


    def integrator_step(self):
        netf_v = np.array([[self.get_netF_aero_prop()], [0], [0]])
        mat_one = np.matmul(np.transpose(self.get_T_vg()), netf_v)

        mat_two = np.dot(self.get_mass(), self.get_gravity())

        mat_one_two = np.add(mat_one, mat_two)

        m_dvdt_i = np.matmul(np.transpose(self.get_T_gi()), mat_one_two)

        dvdt_i = np.dot(1/self.get_mass(), m_dvdt_i)

        self.Acc_mat.append(np.linalg.norm(dvdt_i))


        v_new = self.vb_i_i + np.dot(self.timestep, dvdt_i)
        s_new = self.Sbi + np.dot(self.timestep, self.vb_i_i)
        self.time.append(self.time[-1]+self.timestep)

        #print(self.vb_i_i)

        self.vb_i_i = v_new
        self.Sbi = s_new

        return np.linalg.norm(v_new)


    def integerator(self):
        v = self.integrator_step()
        alt = self.get_altitude()
        v = self.integrator_step()
        new_alt = self.get_altitude()
        while new_alt>alt:
            v = self.integrator_step()
            alt = new_alt
            new_alt = self.get_altitude()
        return self.get_altitude()



rock = Rocket(0)
print(rock.integerator())
print(rock.Acc_mat[-1])
print(rock.cd)