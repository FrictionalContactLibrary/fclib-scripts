#!/usr/bin/env python

#
# Example of one object under gravity with one contactor and a ground
#

from siconos.mechanics.collision.tools import Contactor
from siconos.io.mechanics_run import MechanicsHdf5Runner, MechanicsHdf5Runner_run_options
from siconos.mechanics.collision.bullet import SiconosBulletOptions

import siconos.numerics as Numerics
import siconos.kernel as Kernel
from siconos.io.FrictionContactTrace import GlobalFrictionContactTraceParams


import sys
sys.path.append('../../')

from creation.tools import InputData

from params import *

# Creation of the hdf5 file for input/output
with MechanicsHdf5Runner() as io:

    input_data= InputData(io)
    
    # Definition of a non smooth law. As no group ids are specified it
    # is between contactors of group id 0.
    io.add_Newton_impact_friction_nsl('contact', mu=mu)


import os

base = './PrimitiveSoup'
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

fileName = os.path.join(output_dir,'PrimitiveSoup')
title = "PrimitiveSoup"
description = """
PrimitiveSoup stacking with Bullet collision detection
Moreau TimeStepping Global: h={0}, theta = {1}
One Step non smooth problem: {2}, maxiter={3}, tol={4}
""".format(h, theta,
           Numerics.solver_options_id_to_name(solver_id),
           itermax,
           tolerance)

mathInfo = ""

friction_contact_trace_params = GlobalFrictionContactTraceParams(
    dump_itermax=dump_itermax, dump_probability=dump_probability,
    fileName=fileName, title=title,
    description=description, mathInfo=mathInfo)

# Run the simulation from the inputs previously defined and add
# results to the hdf5 file. The visualisation of the output may be done
# with the vview command.

#T = 417*h

bullet_options = SiconosBulletOptions()

run_options=MechanicsHdf5Runner_run_options()
run_options['t0']=0
run_options['T']=T
run_options['h']=h
run_options['theta']=theta

run_options['Newton_max_iter'] =NewtonMaxIter
run_options['Newton_tolerance'] =1e-10

run_options['bullet_options']=bullet_options
run_options['solver_options']=options

run_options['verbose']=True
#run_options['with_timer']=True
#run_options['explode_Newton_solve']=True
#run_options['explode_computeOneStep']=True

#run_options['violation_verbose'] = True
run_options['output_frequency']=100

run_options['osi']=Kernel.MoreauJeanGOSI

run_options['friction_contact_trace']=True
run_options['friction_contact_trace_params'] = friction_contact_trace_params



with MechanicsHdf5Runner(mode='r+') as io:

    # By default earth gravity is applied and the units are those
    # of the International System of Units.
    # Because of fixed collision margins used in the collision detection,
    # sizes of small objects may need to be expressed in cm or mm.
    # io.run(with_timer=False,
    #        gravity_scale=1,
    #        t0=0,
    #        T=T,
    #        h=h,
    #        theta=theta,
    #        Newton_max_iter=NewtonMaxIter,
    #        solver_options=options,
    #        multipoints_iterations=multipointIterations,
    #        numerics_verbose=False,
    #        output_frequency=100,
    #        osi=Kernel.MoreauJeanGOSI,
    #        friction_contact_trace_params=friction_contact_trace_params,
    #        violation_verbose=True)
    io.run(run_options)
