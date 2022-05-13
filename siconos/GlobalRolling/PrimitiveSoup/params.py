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


# Create solver options
solver_id = (sn.SICONOS_GLOBAL_ROLLING_FRICTION_3D_NSGS_WR)
options = sk.solver_options_create(solver_id)
options.iparam[sn.SICONOS_IPARAM_MAX_ITER] = itermax
options.dparam[sn.SICONOS_DPARAM_TOL] = tolerance
options.iparam[sn.SICONOS_FRICTION_3D_NSGS_FREEZING_CONTACT] = 20

multipointIterations = False
