
cdef class Motor:
  cdef:
    double thrust_avg, time_burnout
    double mass_propellant_initial, mass_total_initial, mass_casing
    bint is_initialised

  cdef void initialise(self, dict motor_props):
    """
    Initialisation function for the Motor class. Stores information related to
    the rocket's propulsion.

    Inputs: A dictionary of motor information, motor_props.
    Outputs: none.
    """
    self.update(motor_props)
    # self.time_burnout = motor_props['time_burnout']
    # self.mass_propellant_initial = motor_props['mass_propellant_initial']
    # self.mass_total_initial = motor_props['mass_total_initial']
    self.mass_casing = self.mass_total_initial - self.mass_propellant_initial
    # self.thrust_avg = motor_props['thrust_avg']
    self.is_initialised = 1

  cdef double getTotalMass(self, double time):
    """
    Gets the total mass of the rocket motor, including casing and propellant.
    Implicitly assumes a linear decrease in propellant mass over the burn time.

    Inputs: A float value time, the time since motor ignition (liftoff).
    Outputs: A float value motor_mass, the total mass of the motor (in kg).
    """
    cdef double motor_mass = self.getPropellantMass(time) + self.mass_casing
    return motor_mass

  cdef double getPropellantMass(self, double time):
    """
    Gets the mass of the remaining unburnt propellant at a given time.
    Assumes a linear burn rate.
    i.e. modelled using the linear function satisying: m(0) = m0, m(t_b) = 0.

    Inputs: A float value time, the time since motor ignition (liftoff).
    Outputs: A float value prop_mass, the mass of propellant remaining (in kg).
    """
    cdef double prop_mass
    if time < self.time_burnout:
      prop_mass = self.mass_propellant_initial * (1 - time/self.time_burnout)
    else:
      prop_mass = 0
    return prop_mass

  cdef double thrust(self, double time):
    """
    Returns the magnitude of the thrust generated by the motor at a given time.
    Assumes the motor thrust is constant from t = 0 to t = t_b, and equal in
    magnitude to the average thrust force of the motor.

    Inputs: A float value time, the time since motor ignition (liftoff).
    Ouputs: A float value thrust_avg, the thrust force generated by the motor (N).
    """
    if time < self.time_burnout:
      return self.thrust_avg
    else:
      return 0



# Python wrapper interface for external access
#===============================================================================
cdef Motor _motor = Motor() # instance of the class to keep hold of data

def initialise(dict motor_dict):
  _motor.initialise(motor_dict)

def getMotorMass(double time):
  return _motor.getTotalMass(time)

def getPropellantMass(double time):
  return _motor.getPropellantMass(time)

def getThrustMagnitude(double time):
  return _motor.thrust(time)