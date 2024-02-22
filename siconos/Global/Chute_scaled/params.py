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

itermax = 1000
NewtonMaxIter = 1
tolerance = 1e-3



solver_id= sn.SICONOS_GLOBAL_FRICTION_3D_NSGS_WR
options = sk.solver_options_create(solver_id)
options.iparam[sn.SICONOS_IPARAM_MAX_ITER] = itermax
options.dparam[sn.SICONOS_DPARAM_TOL] = tolerance
options.iparam[sn.SICONOS_FRICTION_3D_NSGS_FREEZING_CONTACT]=100
int_options=sk.solver_options_get_internal_solver(options,0)

#solver_id =sn.SICONOS_GLOBAL_FRICTION_3D_IPM
# options = sk.solver_options_create(sn.SICONOS_GLOBAL_FRICTION_3D_IPM)
# options.iparam[sn.SICONOS_IPARAM_MAX_ITER] = 1000
# options.dparam[sn.SICONOS_DPARAM_TOL] = tolerance

# solver_id =sn.SICONOS_GLOBAL_FRICTION_3D_ADMM
# options = sk.solver_options_create(solver_id)
# options.iparam[sn.SICONOS_IPARAM_MAX_ITER] = itermax
# options.dparam[sn.SICONOS_DPARAM_TOL] = tolerance

# options.iparam[sn.SICONOS_FRICTION_3D_ADMM_IPARAM_SYMMETRY] =  sn.SICONOS_FRICTION_3D_ADMM_SYMMETRIZE
# #options.iparam[sn.SICONOS_FRICTION_3D_IPARAM_RESCALING]=sn.SICONOS_FRICTION_3D_RESCALING_BALANCING_M

#solver_id= sn.SICONOS_GLOBAL_FRICTION_3D_VI_EG
# options = sk.solver_options_create(solve_id)
# options.iparam[sn.SICONOS_IPARAM_MAX_ITER] = 10000
# options.dparam[sn.SICONOS_DPARAM_TOL] = tolerance

multipointIterations = True
