#!/usr/bin/env python

#
# Example of one object under gravity with one contactor and a ground
#

from siconos.mechanics.collision.tools import Contactor
from siconos.io.mechanics_run import MechanicsHdf5Runner
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
    io.add_Newton_impact_friction_nsl('contact', mu=0.3)



hstep = h
dump_probability = .02

import os

base = './Capsules'
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

fileName = os.path.join(output_dir,'Capsules')
title = "Capsules"
description = """
Capsules stacking with Bullet collision detection
Moreau TimeStepping Global: h={0}, theta = {1}
One Step non smooth problem: {2}, maxiter={3}, tol={4}
""".format(hstep, theta, Numerics.solver_options_id_to_name(solver),
           itermax,
           tolerance)

mathInfo = ""

friction_contact_trace_params = GlobalFrictionContactTraceParams(
    dump_itermax=1, dump_probability=None,
    fileName=fileName, title=title,
    description=description, mathInfo=mathInfo)

# Run the simulation from the inputs previously defined and add
# results to the hdf5 file. The visualisation of the output may be done
# with the vview command.
with MechanicsHdf5Runner(mode='r+') as io:

    # By default earth gravity is applied and the units are those
    # of the International System of Units.
    # Because of fixed collision margins used in the collision detection,
    # sizes of small objects may need to be expressed in cm or mm.
    io.run(with_timer=True,
           gravity_scale=1,
           t0=0,
           T=20.0,
           h=hstep,
           theta=theta,
           Newton_max_iter=1,
           set_external_forces=None,
           solver=solver,
           itermax=itermax,
           tolerance=tolerance,
           numerics_verbose=True,
           output_frequency=None,
           osi=Kernel.MoreauJeanGOSI,
           friction_contact_trace=True,
           friction_contact_trace_params=friction_contact_trace_params)
