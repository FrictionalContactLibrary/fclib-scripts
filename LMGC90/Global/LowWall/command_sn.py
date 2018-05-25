# importing chipy module
from pylmgc90.chipy import *

# Initializing
Initialize()

# checking/creating mandatory subfolders
checkDirectories()

# logMes
# utilities_DisableLogMes()

#
# defining some variables
#

# space dimension
dim = 3

# modeling hypothesis ( 1 = plan strain, 2 = plain stress, 3 = axi-symmetry)
mhyp = 0

# time evolution parameters
dt = 1e-3
nb_steps = 500

# theta integrator parameter
theta = 0.5

# deformable  yes=1, no=0
deformable = 1

# interaction parameters
freq_detect = 1
Rloc_tol = 5.e-2

sn=1

if sn :
 itermax = 5000
 tol = 1.e-12
 relax = 1. #0.25                                                                                                                                                                                                          
 #       123456789012345678901234567890                                                                                                                                                                                    
 solver='globalac                          '
 verbose = 1 # 0: no 1: yes                                                                                                                                                                                                
 output =  3 #0 off, 1 C file, 2 dat, 3 Flib                                                                                                                                                                               
 freq_output = 1 #                                                                                                                                                                                                                
 SiconosNumerics_SetParameters(solver, tol, 100, itermax, relax, verbose, output, freq_output)
 #                                                                                                                                                                                                                         
 idac = timer_GetNewTimer('Siconos')

else:
  # nlgs parameters
  tol = 1e-5
  relax = 1.0
  norm = 'Quad '
  gs_it1 = 500
  gs_it2 = 10
  type='Stored_Delassus_Loops         '
  nlgs_3D_DiagonalResolution()


# write parameter
freq_write   = 10

# display parameters
freq_display = 10
ref_radius = 2.5e-2

# activation du stockage sparse
mecaMAILx_SparseStorage()
# read and load
#

# Set space dimension
SetDimension(dim,mhyp)
#
utilities_logMes('INIT TIME STEPPING')
TimeEvolution_SetTimeStep(dt)
Integrator_InitTheta(theta)
#
utilities_logMes('READ BEHAVIOURS')
ReadBehaviours()
if deformable: ReadModels()
#
utilities_logMes('READ BODIES')
ReadBodies()
#
utilities_logMes('LOAD BEHAVIOURS')
LoadBehaviours()
if deformable: LoadModels()
#
utilities_logMes('READ INI DOF')
ReadIniDof()
#
if deformable:
  utilities_logMes('READ INI GPV')
  ReadIniGPV()
#
utilities_logMes('READ DRIVEN DOF')
ReadDrivenDof()
#
utilities_logMes('LOAD TACTORS')
LoadTactors()
#
utilities_logMes('READ INI Vloc Rloc')
ReadIniVlocRloc()

#
# paranoid writes
#
utilities_logMes('WRITE BODIES')
WriteBodies()
utilities_logMes('WRITE BEHAVIOURS')
WriteBehaviours()
utilities_logMes('WRITE DRIVEN DOF')
WriteDrivenDof()

#
# open display & postpro
#

utilities_logMes('DISPLAY & WRITE')
OpenDisplayFiles()
OpenPostproFiles()

#
# since constant compute elementary mass matrices once
utilities_logMes('COMPUTE MASS')
ComputeMass()

# since constant compute elementary stiffness matrices once
utilities_logMes('COMPUTE STIFFNESS')
ComputeBulk()

# amortissement de Rayleigh
mecaMAILx_ComputeRayleighDamping(0.,0.05)

#PRPRx_CundallIteration(200)
PRPRx_UseCpF2fExplicitDetection(1.e-3) 
PRPRx_ShrinkPolyrFaces(0.05)
PRPRx_LowSizeArrayPolyr(10)

####
# mecaMAILx_SetPreconAllBodies()
# CSxxx_PushPreconNodes()
# ASpxx_PushPreconNodes()
# mecaMAILx_ComputePreconW()

# since constant compute iteration matrix once
AssembleMechanicalLHS()

g_z = 0
for k in range(1, nb_steps + 1, 1):
   #application progressive de la gravite
   if k > 1 and k < 20 : #2000
       g_z += -9.81/18   #1998
       
       print ('xxx')
       print ('incrementation progessive de la gravite : pas num ', k, ', g_z = ', g_z)
       print ('xxx')
       g_x = 0.
       g_y = 0.
       bulk_behav_SetGravity(np.array([g_x,g_y, g_z]))
   #
   utilities_logMes('INCREMENT STEP')
   IncrementStep()
   #
   #utilities_logMes('DISPLAY TIMES')
   #TimeEvolution_DisplayStep()
   #
   utilities_logMes('COMPUTE Fext')
   ComputeFext()
   #
   utilities_logMes('COMPUTE Fint')
   ComputeBulk()
   #
   utilities_logMes('ASSEMBLAGE')
   AssembleMechanicalRHS()
   #
   utilities_logMes('COMPUTE Free Vlocy')
   ComputeFreeVelocity()
   #
   utilities_logMes('SELECT PROX TACTORS')
   SelectProxTactors(freq_detect)
   #
   utilities_logMes('RESOLUTION' )
   #RecupRloc()
   #

   if sn:
     timer_StartTimer(idac)

     SiconosNumerics_ExSolver()

     timer_StopTimer(idac)

   else:
     ExSolver(type, norm, tol, relax, gs_it1, gs_it2)

   UpdateTactBehav()
   #
   StockRloc()
   #
   utilities_logMes('COMPUTE DOF, FIELDS, etc.')
   ComputeDof()
   #
   utilities_logMes('UPDATE DOF, FIELDS')
   UpdateStep()
   #
   utilities_logMes('WRITE OUT DOF')
   WriteOutDof(freq_write)
   #
   utilities_logMes('WRITE OUT GPV')
   WriteOutGPV(freq_write)
   #
   utilities_logMes('WRITE OUT Rloc')
   WriteOutVlocRloc(freq_write)
   #
   utilities_logMes('VISU & POSTPRO')
   WriteDisplayFiles(freq_display,ref_radius)
   WritePostproFiles()

#
# close display & postpro
#
CloseDisplayFiles()
ClosePostproFiles()

# this is the end
Finalize()
