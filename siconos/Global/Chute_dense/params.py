import siconos.numerics as Numerics

t0 = 0
T=10
hstep = 1e-4
g = 9.81
theta = 1.0

#  not used
dump_itermax = 10
dump_probability = .05

itermax = 10000
NewtonMaxIter = 1
tolerance = 1e-3
solver = Numerics.SICONOS_GLOBAL_FRICTION_3D_ADMM
#solver = Numerics.SICONOS_GLOBAL_FRICTION_3D_NSGS_WR
multipointIterations = True

# fileName = "Spheres"
# title = "Spheres"
# description = """
# Spheres falling on the ground with Bullet collision detection
# Moreau TimeStepping: h={0}, theta = {1}
# One Step non smooth problem: {2}, maxiter={3}, tol={4}
# """.format(h, theta, Numerics.idToName(solver),
#            itermax,
#            tolerance)

# mathInfo = ""
