#!/usr/bin/env python

from siconos.io.mechanics_run import MechanicsHdf5Runner
import siconos.numerics as Numerics
import siconos.kernel as Kernel
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

with MechanicsHdf5Runner(mode='w') as io:
    ch = chute.create_chute(io, box_height = box_height,
                            box_length = box_length,
                            box_width = box_width,
                            plane_thickness = plane_thickness,
                            scale = 1, trans = [-0.8, -1.8, -1])

    rcs = rocas.create_rocas(io, n_layer=32, n_row=10, n_col=20,
                             x_shift=1.2, roca_size=0.1, top=3,
                             rate=0.2, density=density)

    io.add_Newton_impact_friction_nsl('contact', mu=1.0, e=0.01)

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
title = "Chute"
description = """
Chute with 6400 polyhedra with Bullet collision detection
Moreau TimeStepping: h={0}, theta = {1}
One Step non smooth problem: {2}, maxiter={3}, tol={4}
""".format(hstep, theta, Numerics.solver_options_id_to_name(solver),
           itermax,
           tolerance)
mathInfo = ""

friction_contact_trace_params = GlobalFrictionContactTraceParams(
    dump_itermax=1, dump_probability=dump_probability,
    fileName=fileName, title=title,
    description=description, mathInfo=mathInfo)
#input()
with MechanicsHdf5Runner(mode='r+', collision_margin=0.01) as io:
    # By default earth gravity is applied and the units are those
    # of the International System of Units.
    # Because of fixed collision margins used in the collision detection,
    # sizes of small objects may need to be expressed in cm or mm.
    io.run(gravity_scale=1.0,
           t0=t0,
           T=T,
           h=hstep,
           multipoints_iterations=multipointIterations,
           theta=theta,
           Newton_max_iter=NewtonMaxIter,
           solver=solver,
           itermax=itermax,
           tolerance=tolerance,
           numerics_verbose=False,
           output_frequency=10,
           osi=Kernel.MoreauJeanGOSI,
           friction_contact_trace=True,
           friction_contact_trace_params=friction_contact_trace_params)
