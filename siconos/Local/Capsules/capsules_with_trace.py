#!/usr/bin/env python

#
# Example of one object under gravity with one contactor and a ground
#

from siconos.mechanics.collision.tools import Contactor
from siconos.io.mechanics_run import MechanicsHdf5Runner
import siconos.numerics as sn
import siconos.kernel as sk
from siconos.io.FrictionContactTrace import FrictionContactTraceParams


import sys
sys.path.append('../../')

from creation.tools import InputData



# Creation of the hdf5 file for input/output
with MechanicsHdf5Runner() as io:

    input_data= InputData(io)
    
    # Definition of a non smooth law. As no group ids are specified it
    # is between contactors of group id 0.
    io.add_Newton_impact_friction_nsl('contact', mu=0.3)


hstep = 0.0005

itermax = 100000
dump_probability = .02
theta = 0.50
tolerance = 1e-8
import os
if not os.path.exists('./Capsules/'):
    os.mkdir('./Capsules/')
    
#solver=Numerics.SICONOS_FRICTION_3D_NSGS

solver_id = sn.SICONOS_FRICTION_3D_NSGS
options = sk.solver_options_create(solver_id)
options.iparam[sn.SICONOS_IPARAM_MAX_ITER] = itermax
options.dparam[sn.SICONOS_DPARAM_TOL] = tolerance






fileName = "./Capsules/Capsules"
title = "Capsules"
description = """
Capsules stacking with Bullet collision detection
Moreau TimeStepping: h={0}, theta = {1}
One Step non smooth problem: {2}, maxiter={3}, tol={4}
""".format(hstep, theta, sn.solver_options_id_to_name(solver_id),
           itermax,
           tolerance)

mathInfo = ""

friction_contact_trace_params = FrictionContactTraceParams(
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
           solver_options=options,
           numerics_verbose=False,
           output_frequency=None,
           friction_contact_trace_params=friction_contact_trace_params)

