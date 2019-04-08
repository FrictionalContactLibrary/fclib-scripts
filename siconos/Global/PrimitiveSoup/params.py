import siconos.numerics as Numerics

t0 = 0
T = 30
h = 0.0005
g = 9.81
theta = 0.50001
mu = 0.7
dump_itermax = 80
dump_probability = .05
itermax = 100
NewtonMaxIter = 20
tolerance = 1e-8
solver = Numerics.SICONOS_GLOBAL_FRICTION_3D_ADMM_WR
#solver = Numerics.SICONOS_GLOBAL_FRICTION_3D_NSGS_WR
multipointIterations = False

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
