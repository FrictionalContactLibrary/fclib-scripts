
from siconos.io.mechanics_run import MechanicsHdf5Runner
import siconos.numerics as sn
import siconos.kernel as sk

import chute
import rocas
import random
import os
from siconos.io.FrictionContactTrace import FrictionContactTraceParams

random.seed(0)

unscaled_cube_size = 0.1
unscaled_plan_thickness = unscaled_cube_size
unscaled_density = 2500

scale = 1.0 / unscaled_cube_size * 10.0

cube_size = unscaled_cube_size * scale
plane_thickness = unscaled_plan_thickness * scale
density = unscaled_density / (scale ** 3)

box_height = 3.683
box_length = 6.900
box_width = 3.430

plane_thickness = 0.2

test = False
if test:
    n_layer = 2
    n_row = 2
    n_col = 2
    step = 200
    hstep = 1e-3
    itermax=1000
else:
    n_layer = 200
    n_row = 2
    n_col = 16
    step = 20000
    hstep = 1e-4
    itermax=2000

# Create solver options
with MechanicsHdf5Runner(mode='w') as io:
    ch = chute.create_chute(io, box_height=box_height,
                            box_length=box_length,
                            box_width=box_width,
                            plane_thickness=plane_thickness,
                            scale=1, trans=[-0.6, -1.8, -1])

    rcs = rocas.create_rocas(io, n_layer=n_layer, n_row=n_row, n_col=n_col,
                             x_shift=2.0, roca_size=0.1, top=3,
                             rate=0.02, density=density)

    io.add_Newton_impact_friction_nsl('contact', mu=1.0, e=0.01)


dump_probability = .02
theta = 1.0
tolerance = 1e-03

from params import *
import os
base = './Chute'
cmp=0
output_dir_created = False
output_dir = base +'_0'
while (not output_dir_created):
    print('output_dir', output_dir)
    if (os.path.exists(output_dir)):
        cmp =cmp+1
        output_dir = base +  '_' + str(cmp)
    else:
        os.mkdir(output_dir)
        output_dir_created = True

fileName = os.path.join(output_dir,'Chute')

options = sk.solver_options_create(sn.SICONOS_GLOBAL_FRICTION_3D_ADMM)
options.iparam[sn.SICONOS_IPARAM_MAX_ITER] = itermax
options.dparam[sn.SICONOS_DPARAM_TOL] = tolerance
fileName = "./Chute/Chute"
title = "Chute"
description = """
Chute with 6400 polyhedra with Bullet collision detection
Moreau TimeStepping: h={0}, theta = {1}
One Step non smooth problem: {2}, maxiter={3}, tol={4}
""".format(hstep, theta, sk.solver_options_id_to_name(options.solverId),
           itermax,
           tolerance)
mathInfo = ""

friction_contact_trace_params = FrictionContactTraceParams(
    dump_itermax=2000, dump_probability=None,
    fileName=fileName, title=title, description=description,
    mathInfo=mathInfo)

with MechanicsHdf5Runner(mode='r+', collision_margin=0.01) as io:
    # By default earth gravity is applied and the units are those
    # of the International System of Units.
    # Because of fixed collision margins used in the collision detection,
    # sizes of small objects may need to be expressed in cm or mm.
    if test:
        io.run(gravity_scale=1.0 / scale,
               t0=0,
               T=step * hstep,
               h=hstep,
               multipoints_iterations=True,
               theta=1.0,
               Newton_max_iter=1,
               output_frequency=10,
               osi=sk.MoreauJeanGOSI,
               solver_options=options)
    else:
        io.run(gravity_scale=1.0 / scale,
               t0=0,
               T=step * hstep,
               h=hstep,
               multipoints_iterations=True,
               theta=1.0,
               Newton_max_iter=1,
               output_frequency=10,
               osi=sk.MoreauJeanGOSI,
               solver_options=options,
               friction_contact_trace_params=friction_contact_trace_params)
