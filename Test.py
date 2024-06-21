from vpython import *

# Constants
G = 6.67e-11
RE = 6.378e6
ME = 5.972e24

# Create Earth object
Earth = sphere(pos=vector(-RE, 0, 0), radius=RE, texture=textures.earth)
Earth.m = ME
Earth.p = Earth.m * vector(0, 0, 0)

# Create satellite object
sat = sphere(pos=vector(2 * RE, 0, 0), radius=0.03 * RE, make_trail=True)
sat.m = 100
sat.p = sat.m * vector(0, 5000, 0)

# Simulation parameters
t = 0
dt = 1

# Simulation loop
while t < 10000:
    rate(400)
    # Calculate distance between satellite and Earth
    r = sat.pos - Earth.pos
    # Calculate gravitational force
    F = -G * Earth.m * sat.m * norm(r) / mag(r)**2
    # Update satellite momentum
    sat.p = sat.p + F * dt
    # Update satellite position
    sat.pos = sat.pos + sat.p * dt / sat.m
    # Update time
    t = t + dt