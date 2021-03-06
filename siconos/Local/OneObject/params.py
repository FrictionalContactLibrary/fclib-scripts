import Siconos.Numerics as Numerics

t0 = 0
T = 10
h = 0.0005
g = 9.81
theta = 0.50001
mu = 0.7
dump_itermax = 50
dump_probability = .9
NewtonMaxIter = 20
itermax = 100000
tolerance = 1e-8
solver = Numerics.SICONOS_FRICTION_3D_NSGS


fileName = "OneObject"
title = "OneObject"
description = """
One Box 1 100 5 falling on the ground with Bullet collision detection
Moreau TimeStepping: h={0}, theta = {1}
One Step non smooth problem: {2}, maxiter={3}, tol={4}
""".format(h, theta, Numerics.idToName(solver),
           itermax,
           tolerance)

mathInfo = ""
