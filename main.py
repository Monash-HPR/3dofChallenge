import logging
import numpy as np
import matplotlib.pyplot as plt

# This should be before the Modules import so the logging level is shared
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

from Modules import Integrator, Aerodynamics, Propulsion, State, Atmosphere, Gravity
logger.debug('All Modules Loaded')

class Simulator:
    def __init__(self, diameter, mass, step=0.001, max_iters=10000):
        logger.debug('Creating Simulator Instance')

        self.iters = 0
        self.reached_apogee = False

        self.step = step
        self.max_iters = max_iters
        self.mass = mass
        self.diameter = diameter
        self.motor = Propulsion.BasicMotor(
            average_thrust=999.0,
            propellant_mass=0.147,
            total_mass=0.331,
            burnout_time=0.3,
        )
        self.drag = Aerodynamics.Drag(diameter=self.diameter)
        self.gravity = Gravity.Gravity()
        self.state = State.State()
        self.integrator = Integrator.Integrator(step=self.step)

    def initialise(self):
        logger.info('Initialising Simulator')

    def run(self):
        logger.info('Running Simulator')
        states = [self.state.copy()]

        while not self.reached_apogee:
            _state = self.state.copy()
            self.integrator.RK4(_state, self.get_accel)
            _state.update(
                mass=self.motor.get_mass(_state.time),
                drag=self.drag.get_force(_state.vel, _state.alt),
                gravity=self.gravity.get_force(_state.alt, self.mass + self.motor.get_mass(_state.time))
            )
            self.state.update_from(_state)
            self.iters += 1
            states.append(_state)
            if self.iters > self.max_iters or self.state.alt <= 0:
                self.reached_apogee = True

        output = np.array([[s.time, s.alt] for s in states])
        plt.plot(output.T[0], output.T[1])
        plt.show()
        logger.info('Finished Simulator')

    def get_accel(self, time, vel, alt):
        mass = self.mass + self.motor.get_mass(time)
        net_force = self.motor.get_thrust(time) - np.multiply(np.sign(vel), np.abs(self.drag.get_force(vel, alt))) - self.gravity.get_force(alt, mass)
        #print(net_force, self.motor.get_thrust(time), np.abs(self.drag.get_force(vel, alt)), self.gravity.get_force(alt, mass), vel, alt)
        return net_force/mass

if __name__ == "__main__":
    logger.info('Starting 3DOF Simulator')
    sim = Simulator(
        diameter=0.0762,
        mass=0.454
    )
    sim.initialise()
    sim.run()
