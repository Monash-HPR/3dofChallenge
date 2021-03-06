# 3dofChallenge
Dynamics section challenge to each individually develop a 3 degree-of-freedom
(3DoF) simulation from 7/5/2019 to 28/5/2019.

This description is a work in progress, and will be updated as the task
progresses.

Each team member will be expected to develop a 3DoF simulation which can:
  1) Demonstrate translation in all 3 axes over the the course of a rocket
      flight.
  2) Produce readable/usable numerical results and figures to assess the success
      of the rocket's flight, in an appropriate reference frame and with
      reasonable choices made for units.
  3) Produce results that are comparable with the OpenRocket file and current
      Saturn simulation for a small subsonic rocket.


As part of a complete simulation, it is expected that:
  1) The simulation models all relevant physical/environmental effects to an
      appropriate extent, given time and information access constraints on the
      task.
  2) The simulation is based on Zipfel's formulation (or another book, provided
      it is approved and justified), and uses the standard notation developed
      to express tensor equations in code (will be explained later).
  3) The progress of the simulation can be seen over time by commits to the
      appropriate Git repository, with full commit messages.
  4) The sim files include a module/file for testing purposes, and enough tests
      to confirm the preliminary validity of your simulation
  5) All functions contain sufficient documentation to explain their purpose,
      function, and appropriate inputs/outputs.
  6) The simulation sanitises inputs/checks error cases where possible, within
      reason.


Challenge:
After submission, the simulations will be assessed for efficiency (time and
space), accuracy, innovation in terms of the simulation structure - with
particular weight on the 'extra' module.
It is in your best interested to Cythonize as much as possible, decompose code
where possible, and strongly consider the structure of your simulation before
beginning implementation.

Modelling Simplifications:
Several simplifications are allowed to reduce the task of modelling sections that are not your 'extra':
  1) Centre of gravity or centre of pressure calculations are not required unless this is your 'extra'.
  2) Motor mass change can me modelled as linear (from m(0)=m0 to m(t_burnout)=0).
  3) Motor mass calculations must allow for some non-zero mass of the motor casing, for use in calculating the total rocket
     mass.
  4) Motor thrust can be assumed constant, and equal to the average rated thrust of the motor for the duration of the burn.
  5) Aerodynamic drag coefficient can be modelled using: c_D(M) = 2400 * (exp(-1.2M) * sin(M) + (M/6) * log_{10}(M+1)).
    (This is temporary and this model will be updated, watch this space. The new model will be of similar complexity.)
    Reference area should be taken as the cross-sectional area of the rocket at the base of the nosecone, and it can be 
    expected that this diameter or radius will be given.

Rules:
The rules below will operate on an honour policy. The point of the challenge is
to generate innovative approaches for dealing with our problems. Not abiding by
these rules will limit your creativity and the value derived from this task.
  1) Each person's challenge must be on a separate branch of this directory.
  2) Looking at/copying the existing implementation of Saturn, or any other
      person's implementation of the task, is forbidden.
  3) tbc.

Timeline:
7/5: Challenge issued
14/5: Preliminary assessment of 'core' 3DoF functions
21/5: Final 3DoF function completion
28/5: 'Extra' module completed and overall project assessment


'Extra' module allocations:
Hamish: Aerodynamics
Ciaran: Fin flutter
Amjed: Parachutes
Kenneth: Weather
Matt: Ballast calculator
Emily: Body Geometry
Caleb: Dynamics on the launch rail


Last updated: 9/5/2019
Updated by: Hamish Self
