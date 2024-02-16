import siconos.numerics as sn
import siconos.kernel as sk

t0 = 0
T = 30
h = 0.0005
g = 9.81
theta = 0.50001
mu = 0.7
dump_itermax = 80
dump_probability = .05
itermax = 100
NewtonMaxIter = 1
tolerance = 1e-8



solver = sn.SICONOS_GLOBAL_FRICTION_3D_ADMM
options = sk.solver_options_create(solver)
options.iparam[sn.SICONOS_IPARAM_MAX_ITER] = itermax
options.dparam[sn.SICONOS_DPARAM_TOL] = tolerance

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
