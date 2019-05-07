# Main sim loop and associated setup/initialisation
from Integrator import *
from Structures import *

s = State()
print(s.a)
s = integrate_Rk4(s)
print(s.a)
