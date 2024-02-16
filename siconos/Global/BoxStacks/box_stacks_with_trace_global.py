#!/usr/bin/env python

import os

from siconos.mechanics.collision.tools import Contactor
from siconos.io.mechanics_run import MechanicsHdf5Runner, MechanicsHdf5Runner_run_options
from siconos.mechanics.collision.bullet import SiconosBulletOptions
import siconos.numerics as Numerics
import siconos.kernel as Kernel
from siconos.io.FrictionContactTrace import FrictionContactTraceParams

# A collection of box stacks for stress-testing Siconos solver with
# chains of contacts.

# Creation of the hdf5 file for input/output
with MechanicsHdf5Runner() as io:

    width, depth, height = 1, 1, 1
    io.add_primitive_shape('Box', 'Box', [width, depth, height])

    k = 0
    sep = 0.01

    def make_stack(X, Y, N, M, W):
        global k
        z = height/2.0
        while W > 0:
            for i in range(N):
                for j in range(M):
                    x = (i-N/2.0)*(width+sep) + X
                    y = (j-M/2.0)*(depth+sep) + Y
                    io.add_object('box%03d' % k, [Contactor('Box')],
                                  translation=[x,y,z],
                                  mass=1.0)
                    k += 1
            N = N - 1 if N > 1 else N
            M = M - 1 if M > 1 else M
            W = W - 1
            z += height + sep

    # A column
    make_stack(0, -10, 1, 1, 5)

    # A pyramid
    make_stack(0, 0, 5, 5, 5)

    # A wall
    make_stack(0, 10, 1, 5, 5)

    # Definition of the ground
    io.add_primitive_shape('Ground', 'Box', (50, 50, 0.1))
    io.add_object('ground', [Contactor('Ground')], [0, 0, -0.05])

    # Enable to smash the wall
    # io.add_primitive_shape('Ball', 'Sphere', [1,])
    # io.add_object('WreckingBall', [Contactor('Ball')],
    #              translation=[30,0,3], velocity=[-30,0,2,0,0,0],
    #              mass=10)

    # Definition of a non smooth law. As no group ids are specified it
    # is between contactors of group id 0.
    io.add_Newton_impact_friction_nsl('contact', mu=0.3)
solver = Numerics.SICONOS_GLOBAL_FRICTION_3D_ADMM

step = 125
hstep = 1e-2
itermax = 1000
dump_probability = .02
theta = 0.50
tolerance = 1e-12
base = './BoxStacks'
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

fileName = os.path.join(output_dir,'BoxStacks')
title = "Box_stacks"
description = """
Box stacks with Bullet collision detection
Moreau TimeStepping Global: h={0}, theta = {1}
One Step non smooth problem: {2}, maxiter={3}, tol={4}
""".format(hstep, theta, Numerics.solver_options_id_to_name(solver),
           itermax,
           tolerance)

mathInfo = ""

friction_contact_trace_params = FrictionContactTraceParams(
    dump_itermax=20, dump_probability=None,
    fileName=fileName, title=title,
    description=description, mathInfo=mathInfo)



options = Kernel.solver_options_create(Numerics.SICONOS_GLOBAL_FRICTION_3D_ADMM)
options.iparam[Numerics.SICONOS_IPARAM_MAX_ITER] = itermax
options.dparam[Numerics.SICONOS_DPARAM_TOL] = tolerance
options.iparam[Numerics.SICONOS_FRICTION_3D_NSGS_FREEZING_CONTACT] = 0




run_options=MechanicsHdf5Runner_run_options()
run_options['t0']=0
run_options['T']=step*hstep
run_options['h']=hstep
run_options['theta']=theta

run_options['Newton_max_iter'] =1
run_options['Newton_tolerance'] =1e-10

#run_options['bullet_options']=bullet_options
run_options['solver_options']=options

run_options['verbose']=True
#run_options['with_timer']=True
#run_options['explode_Newton_solve']=True
#run_options['explode_computeOneStep']=True

#run_options['violation_verbose'] = True
run_options['output_frequency']=1

run_options['osi']=Kernel.MoreauJeanGOSI

run_options['friction_contact_trace']=True
run_options['friction_contact_trace_params'] = friction_contact_trace_params


# # Load and run the simulation
# with MechanicsHdf5Runner(mode='r+') as io:
#     io.run(t0=0,
#            T=step*hstep,
#            h=hstep,
#            theta=theta,
#            Newton_max_iter=1,
#            solver=Numerics.SICONOS_GLOBAL_FRICTION_3D_ADMM,
#            itermax=itermax,
#            tolerance=tolerance,
#            output_frequency=1,
#            osi=Kernel.MoreauJeanGOSI,
#            friction_contact_trace=True,
#            friction_contact_trace_params=friction_contact_trace_params)
with MechanicsHdf5Runner(mode='r+') as io:
     io.run(run_options)
