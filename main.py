import logging
import numpy as np
import matplotlib.pyplot as plt

# This should be before the Modules import so the logging level is shared
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

from Modules import Integrator, Aerodynamics, Propulsion, State, Atmosphere, Gravity, Transformations
logger.debug('All Modules Loaded')

class Simulator:
    def __init__(
            self,
            diameter,
            mass,
            launch_rail_length=4.0,
            launch_rail_mu=100.0,
            launch_rail_mu_static=1000.0,
            step=0.001,
            max_iters=100000
        ):
        logger.debug('Creating Simulator Instance')

        self.iters = 0
        self.reached_end = False
        self.reached_apogee = False

        self.launch_rail_mu = launch_rail_mu
        self.launch_rail_mu_static = launch_rail_mu_static
        self.launch_rail_length = launch_rail_length
        self.step = step
        self.max_iters = max_iters
        self.mass = mass
        self.diameter = diameter
        self.motor = Propulsion.BasicMotor(
            average_thrust=838.9,
            propellant_mass=4.436,
            total_mass=6.954,
            burnout_time=9.0,
        )
        self.drag = Aerodynamics.Drag(diameter=self.diameter)
        self.gravity = Gravity.Gravity()
        self.state = State.State()
        self.integrator = Integrator.Integrator(step=self.step)
        [self.lat, self.lon] = -37.8136, 144.9631 # Initialise location

    def initialise(self):
        logger.info('Initialising Simulator')

    def run(self):
        logger.info('Running Simulator')
        states = [self.state.copy()]

        while not self.reached_end:
            _state = self.state.copy()
            self.integrator.RK4(_state, self.get_accel)
            _state.update(
                mass=self.motor.get_mass(_state.time),
                drag=self.drag.get_force(_state.vel, _state.pos),
                gravity=self.gravity.get_acceleration(_state.pos[1])*self.motor.get_mass(_state.time)
            )
            self.state.update_from(_state)
            self.iters += 1

            states.append(_state)
            if self.state.pos[1] < states[-2].pos[1]:
                self.reached_apogee = True
            if self.iters > self.max_iters or self.state.pos[1] <= 0:
                self.reached_end = True

        logger.info('Finished Simulator')
        [time, pos, vel, acc, drag, grav] = np.array([[s.time, s.pos[1], s.vel[1], s.acc[1], s.drag[1], s.gravity[1]] for s in states]).T
        print(f'Max Alt: {np.max(pos):.3f} m')
        print(f'Max Vel: {np.max(vel):.3f} m/s')
        print(f'Max Acc: {np.max(acc):.3f} m/s^2')

        plt.subplot(2, 2, 1)
        plt.plot(time, pos)
        plt.xlabel('Time [s]')
        plt.ylabel('Altitude [m]')

        plt.subplot(2, 2, 2)
        plt.plot(time, vel)
        plt.xlabel('Time [s]')
        plt.ylabel('Velocity [m/s]')

        plt.subplot(2, 2, 3)
        plt.plot(time, acc)
        plt.xlabel('Time [s]')
        plt.ylabel('Acceleration [m/s^2]')

        """plt.subplot(2, 2, 4)
        plt.xlabel('Time [s]')
        plt.ylabel('Position (Inertial) [m]')
        plt.legend(['0^I', '2^I'])"""

        plt.tight_layout()
        plt.show()

    def get_accel(self, time, vel, pos):
        """
        Get the acceleration w.r.t inertial frame

        :param state: The current state to use
        :type state: Modules.State.State
        :param accel_func:
        :type accel_func: Callable with 2 arguments (time, alt)

        """
        mass = self.mass + self.motor.get_mass(time)

        # Calculate specific force w.r.t. body
        contact_force = self.motor.get_thrust(time) + self.drag.get_force(vel, pos)
        specific_force = contact_force/mass

        # NOTE: Hardcoding [yaw,pitch,roll] as [0,0,0] as this is a 3DOF sim
        [yaw, pitch, roll] = [0.0, 0.0, 0.0]
        # Change the specific force to geocentric
        specific_force_G = Transformations.T_GB(yaw, pitch, roll) @ specific_force
        # Calculate the net acceleration w.r.t. geocentric
        accel_G = specific_force_G + self.gravity.get_acceleration(pos[1])

        # Check if the body is still on the launch rail
        if (Transformations.T_GI(time, self.lat, self.lon) @ pos)[1] <= self.launch_rail_length and not self.reached_apogee:
            # Calculate the net specific force acting perpendicular to the launch rail
            spec_force_rail = np.array([accel_G[0], 0.0, accel_G[2]])
            spec_force_rail_mag = np.linalg.norm(spec_force_rail)

            # Calculate the friction against the launch rail
            # Modified friction formula for specific force rather than total force
            spec_force_rail_friction = -np.sign(vel[1]) * spec_force_rail_mag * self.launch_rail_mu
    
            # Add the friction to the net acceleration, whilst ensuring the acceleration doesn't go negative
            # NOTE: Possible bug here, if motor burns out before off the launch rail then the body will `hover`
            #accel_G[1] = np.max([accel_G[1] + spec_force_rail_friction, 0.0])
            accel_G[1] = accel_G[1] + spec_force_rail_friction

            # Prevent acceleration in the 1^G and 3^G axes
            accel_G[0] = 0.0
            accel_G[2] = 0.0

        # Change the net acceleration to inertial coordinates
        accel_I = Transformations.T_IG(time, self.lat, self.lon) @ accel_G
        return accel_G

if __name__ == "__main__":
    logger.info('Starting 3DOF Simulator')
    sim = Simulator(
        diameter=0.131,
        mass=16.194,
        launch_rail_length=4,
        max_iters=2000000
    )
    sim.initialise()
    sim.run()
