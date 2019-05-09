# motor code goes here

# thrust
# decrease in mass
# change in motor c.g. (?)

cdef class Motor:
  cdef:
    double thrust_avg, time_burnout
    double mass_propellant_initial, mass_total_initial, mass_casing

  def initialise(self, dict motor_props):
    self.time_burnout = motor_props['time_burnout']
    self.mass_propellant_initial = motor_props['mass_propellant_initial']
    self.mass_total_initial = motor_props['mass_total_initial']
    self.mass_casing = self.mass_total_initial - self.mass_propellant_initial
    self.thrust_avg = motor_props['thrust_avg']

  def getTotalMass(self, double time): # FIX TO DEAL WITH CASING MASS
    # linear decrease in motor mass:
    # m(0) = m0, m(t_b) = 0
    cdef double motor_mass = self.getPropellantMass(time) + self.mass_casing
    return motor_mass

  def getPropellantMass(self, double time):
    cdef double prop_mass
    if time < self.time_burnout:
      prop_mass = self.mass_propellant_initial * (1 - time/self.time_burnout)
    else:
      prop_mass = 0
    return prop_mass

  def thrust(self, double time):
    # constant average thrust for the motor until burnout
    # USE BODY COORDINATES AND RETURN THRUST VECTOR???
    if time < self.time_burnout:
      return self.thrust_avg
    else:
      return 0


cdef Motor _motor = Motor()


# Python interface
def initialise(dict motor_dict):
  _motor.initialise(motor_dict)

def getMotorMass(double time):
  return _motor.getTotalMass(time)

def getPropellantMass(double time):
  return _motor.getPropellantMass(time)

def getThrustMagnitude(double time):
  return _motor.thrust(time)
