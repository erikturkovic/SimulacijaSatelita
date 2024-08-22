from vpython import *

G = 6.67e-11
RE = 6.378e6
ME = 5.972e24

Earth = sphere(pos=vector(-RE, 0, 0), radius=RE, texture=textures.earth)
Earth.m = ME

def create_satellite(pos, velocity, mass, radius):
    sat = sphere(pos=pos, radius=radius, make_trail=True)
    sat.m = mass
    sat.p = sat.m * velocity
    return sat

def update_position(sat, dt):
    r = sat.pos - Earth.pos
    F = -G * Earth.m * sat.m * norm(r) / mag(r)**2
    sat.p = sat.p + F * dt
    sat.pos = sat.pos + sat.p * dt / sat.m

satellites = [
    create_satellite(vector(2 * RE, 0, 0), vector(0, 5000, 0), 100, 0.03 * RE),
    create_satellite(vector(2 * RE, 10, 15), vector(1000, 5000, 2000), 100, 0.03 * RE)
]

def run_simulation(satellites, dt):
    while True:
        rate(400)
        for sat in satellites:
            update_position(sat, dt)

run_simulation(satellites, 1)