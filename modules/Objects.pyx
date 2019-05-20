class Rocket():
  __slots__ = ["position", "velocity", "history", "time"] # preallocating - performance trick
  def __init__ (self, position, velocity, history, time):
    # position, velocity are 3x1 vectors, history is a 2xn (n being number of timesteps) sized vector.
    self.position = position
    self.velocity = velocity
    self.history = history
    self.time = time

  def saveHistory(self):
    self.history.append([self.position, self.velocity])

  
