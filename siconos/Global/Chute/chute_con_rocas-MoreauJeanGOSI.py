#!/usr/bin/env python
import siconos.numerics as sn
import siconos.kernel as sk
from siconos.io.mechanics_run import MechanicsHdf5Runner

from siconos.io.FrictionContactTrace import GlobalFrictionContactTraceParams

import chute
import rocas
import random

random.seed(0)

cube_size = 0.1
plan_thickness = cube_size
density = 2500

#print('density',density)

box_height = 3.683
box_length = 6.900
box_width  = 3.430

plane_thickness = 0.2


from params import *


test = False
if test:
    n_layer = 20
    n_row = 4
    n_col = 4
    step = 100
    hstep = 1e-3
    itermax=100
    options.iparam[sn.SICONOS_IPARAM_MAX_ITER] = itermax
    options.dparam[sn.SICONOS_DPARAM_TOL] = tolerance
else:
    n_layer = 100
    n_row = 4
    n_col = 16


with MechanicsHdf5Runner(mode='w') as io:
    ch = chute.create_chute(io, box_height=box_height,
                            box_length=box_length,
                            box_width=box_width,
                            plane_thickness=plane_thickness,
                            scale=1, trans=[-0.6, -1.8, -1])

    # The time of death is driven by the rate value.
    # For a layer, number n, the time of birth is given by n*rate+random.random()*rate*2/5
    # The travel time for a grain is 0.5*9.81*(rate)**2
    
    rcs = rocas.create_rocas(io, n_layer=n_layer, n_row=n_row, n_col=n_col,
                             x_shift=2.0, roca_size=0.1, top=3,
                             rate=0.25, density=density)

    io.add_Newton_impact_friction_nsl('contact', mu=1.0, e=0.01)


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


print('itermax', itermax)
sn.numerics_set_verbose(2)
sk.solver_options_print(options)
title = "Chute"
description = """
Chute with 6400 polyhedra with Bullet collision detection
Moreau TimeStepping: h={0}, theta = {1}
One Step non smooth problem: {2}, maxiter={3}, tol={4}
""".format(hstep,
           theta,
           sk.solver_options_id_to_name(solver_id),
           itermax,
           tolerance)
mathInfo = ""

friction_contact_trace_params = GlobalFrictionContactTraceParams(
    dump_itermax=1, dump_probability=None,
    fileName=fileName, title=title,
    description=description, mathInfo=mathInfo)
with MechanicsHdf5Runner(mode='r+', collision_margin=0.01) as io:
    # By default earth gravity is applied and the units are those
    # of the International System of Units.
    # Because of fixed collision margins used in the collision detection,
    # sizes of small objects may need to be expressed in cm or mm.
    if test:
        io.run(gravity_scale=1.0,
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
    else:
        io.run(gravity_scale=1.0,
               t0=0,
               T=step * hstep,
               h=hstep,
               multipoints_iterations=True,
               theta=1.0,
               Newton_max_iter=1,
               output_frequency=10,
               osi=sk.MoreauJeanGOSI,
               solver_options=options,
               numerics_verbose=True,
               friction_contact_trace_params=friction_contact_trace_params)
