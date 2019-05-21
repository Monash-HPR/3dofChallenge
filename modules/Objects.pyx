class rocketState:
  __slots__ = ["position", "velocity", "history", "time"] # preallocating - performance trick
  def __init__ (self, position, velocity, history, time):
    # position, velocity are 3x1 vectors, history is a 2xn (n being number of timesteps) sized vector.
    self.position = position
    self.velocity = velocity
    self.history = history
    self.time = time

  def saveHistory(self):
    self.history.append([self.position, self.velocity])

  def updateTime(self, new_time):
    self.time = new_time

  def __str__(self):
    strpos = '[' + ','.join(str(comp) for comp in self.position) + ']'
    strvel = '[' + ','.join(str(comp) for comp in self.velocity) + ']'
    return "Position: %s, Velocity: %s, Time: %s" % (strpos, strvel, self.time)

class rocketParams:
  __slots__ = ["diameter", "avgthrust", "mass_fuel", "mass_start", "burnout_time", "time", "mass"]
  def __init__ (self, diameter, time):
    # diameter mass and time are all numbers, motorthurst is a 3x1 vector.
    self.diameter = diameter
    self.avgthrust = 838 # Cesaroni M840
    self.mass_fuel = 4.249
    self.mass_start = 24.704
    self.burnout_time = 9
    self.time = time
    self.mass = self.mass_start - (self.mass_fuel)*(self.time/self.burnout_time) #linear rate

  def __str__(self):
    return ("Diameter: %s, Thrust: %s, Fuel mass: %s, Start mass: %s, Burnout time: %s, Time: %s, Current mass: %s"
    % (self.diameter, self.avgthrust, self.mass_fuel, self.mass_start, self.burnout_time, self.time, self.mass))

  def updateTime(self, new_time):
    self.time = new_time
    if self.burnout_time < self.time:
      self.avgthrust = 0
    self.mass = self.mass_start - (self.mass_fuel)*(self.time/self.burnout_time)
