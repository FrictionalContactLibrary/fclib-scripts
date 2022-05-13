import siconos.numerics as sn
import siconos.kernel as sk
t0 = 0
hstep = 1e-4
step=10e5
T=step*hstep
g = 9.81
theta = 1.0

#  not used
dump_itermax = 10
dump_probability = .05

itermax = 100
NewtonMaxIter = 1
tolerance = 1e-3

# Create solver options
solver_id = (sn.SICONOS_GLOBAL_ROLLING_FRICTION_3D_NSGS_WR)
options = sk.solver_options_create(solver_id)
options.iparam[sn.SICONOS_IPARAM_MAX_ITER] = itermax
options.dparam[sn.SICONOS_DPARAM_TOL] = tolerance
options.iparam[sn.SICONOS_FRICTION_3D_NSGS_FREEZING_CONTACT] = 20


multipointIterations = True
