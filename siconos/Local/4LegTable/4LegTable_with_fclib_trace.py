#!/usr/bin/env python

#
# Example of one object under gravity with one contactor and a ground
# using the Siconos proposed mechanics API
#

from siconos.mechanics.collision.tools import Contactor, Volume
from siconos.io.mechanics_run import MechanicsHdf5Runner
import siconos.numerics as Numerics
from siconos.io.FrictionContactTrace import FrictionContactTraceParams
import math
import numpy as np
# Creation of the hdf5 file for input/output
with MechanicsHdf5Runner() as io:

    # Definition of a capsule
    R = 0.05
    L = .7
    io.add_primitive_shape('leg', 'Sphere', (R, ))

    # Definition of the ground shape
    io.add_primitive_shape('Ground', 'Box', (10, 10, 0.5))
    
    # Definition of the ground shape
    io.add_primitive_shape('Table', 'Box', (1, 1, .1))

    # Definition of a non smooth law. As no group ids are specified it
    # is between contactors of group id 0.
    io.add_Newton_impact_friction_nsl('contact', mu=0.7, e=0.1)

    # The sphere object made with an unique Contactor : the sphere shape.
    # As a mass is given, it is a dynamic system involved in contact
    # detection and in the simulation.  With no group id specified the
    # Contactor belongs to group 0
    mass_test = 1.0
    inertia_test = np.eye(3)

    inertia_test[0, 0] = 0.25*mass_test*R*R + 1/3.0*mass_test*L*L
    inertia_test[1, 1] = 0.5*mass_test*R*R
    inertia_test[2, 2] = 0.25*mass_test*R*R + 1/3.0*mass_test*L*L
    print(inertia_test)
    orientation_test = [1.0, 0.0, 0.0, 0]

    io.add_object('table', [Contactor('Table'),
                            Contactor(shape_name='leg', instance_name='leg_1',
                                      relative_translation=[0.5,0.5,-.7],
                                      relative_orientation = [math.sqrt(2.)/5., 0.0, math.sqrt(2.)/5., 0.0]),
                            Contactor(shape_name='leg', instance_name='leg_2',
                                      relative_translation=[-0.5,0.5,-.7], relative_orientation = [math.sqrt(2.)/2., 0.0, math.sqrt(2.)/2., 0.0]),
                            Contactor(shape_name='leg', instance_name='leg_3',
                                      relative_translation=[0.5,-0.5,-.7], relative_orientation = [math.sqrt(2.)/2., 0.0, math.sqrt(2.)/2., 0.0]), 
                            Contactor(shape_name='leg', instance_name='leg_4',
                                      relative_translation=[-0.5,-0.5,-.7], relative_orientation = [math.sqrt(2.)/2., 0.0, math.sqrt(2.)/2., 0.0])],
                  orientation=orientation_test,
                  velocity=[0, 5, 0, 0, 0, 0],
                  mass=1, inertia=inertia_test)
 
    # the ground object made with the ground shape. As the mass is
    # not given, it is a static object only involved in contact
    # detection.
    io.add_object('ground', [Contactor('Ground')],
                  translation=[0, 0, -2.0])

hstep = 5e-4
itermax = 10000
dump_probability = .02
theta = 0.50
tolerance = 1e-6
newton_itermax=20




import os

base = './4LegsTable'
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

fileName = os.path.join(output_dir,'Spheres')
    
solver=Numerics.SICONOS_FRICTION_3D_NSGS
title = "4 legs table"
description = """
Moreau TimeStepping: h={0}, theta = {1}
One Step non smooth problem: {2}, maxiter={3}, tol={4}
""".format(hstep, theta, Numerics.solver_options_id_to_name(solver),
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
    io.run(with_timer=False,
           face_class=None,
           edge_class=None,
           t0=0,
           T=2,
           h=hstep,
           multipoints_iterations=False,
           theta=theta,
           Newton_max_iter=newton_itermax,
           set_external_forces=None,
           solver=Numerics.SICONOS_FRICTION_3D_NSGS,
           itermax=itermax,
           tolerance=tolerance,
           numerics_verbose=False,
           output_frequency=None,
           friction_contact_trace=True,
           friction_contact_trace_params=friction_contact_trace_params)
