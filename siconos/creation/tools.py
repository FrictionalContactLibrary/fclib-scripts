
import shlex, os
import numpy as np
from siconos.mechanics.collision.tools import Contactor
from siconos.mechanics.collision.bullet import btVector3, \
    btConvexHullShape, btCylinderShape, btBoxShape, btSphereShape, \
    btConeShape, btCapsuleShape, btCompoundShape, btTriangleIndexVertexArray, \
    btGImpactMeshShape
try:
    import vtk
except:
    pass
#
# load .vtp file
#
def loadMesh(shape_filename):
    """
    loads a vtk .vtp file and returns a Bullet concave shape
    WARNING triangles cells assumed!
    """

    reader = vtk.vtkXMLPolyDataReader()
    reader.SetFileName(shape_filename)
    reader.Update()

    polydata = reader.GetOutput()
    points = polydata.GetPoints().GetData()
    num_points = points.GetNumberOfTuples()
    num_triangles = polydata.GetNumberOfCells()

    keep = None
    shape = None

    if polydata.GetCellType(0) == 5:
        apoints = np.empty((num_points, 3))
        for i in range(0, points.GetNumberOfTuples()):
            p = points.GetTuple(i)
            apoints[i, 0] = p[0]
            apoints[i, 1] = p[1]
            apoints[i, 2] = p[2]

        aindices = np.empty((num_triangles, 3), dtype=np.int32)

        for i in range(0, num_triangles):
            c = polydata.GetCell(i)
            aindices[i, 0] = c.GetPointIds().GetId(0)
            aindices[i, 1] = c.GetPointIds().GetId(1)
            aindices[i, 2] = c.GetPointIds().GetId(2)

        tri = btTriangleIndexVertexArray(apoints, aindices)

        shape = btGImpactMeshShape(tri)
        shape.updateBound()

        keep = tri, apoints, aindices

    else:  # assume convex shape
        coors = dict()
        apoints = np.empty((num_points, 3))
        for i in range(0, points.GetNumberOfTuples()):
            p = points.GetTuple(i)
            apoints[i, 0] = p[0]
            apoints[i, 1] = p[1]
            apoints[i, 2] = p[2]
            coors[points.GetTuple(i)] = 1
            
        shape = btConvexHullShape()
        keep = apoints
        for p in coors:
                shape.addPoint(btVector3(*p))
        #print(coors)
    return keep, shape

class ShapeCollection():

    """
    collect Bullet primitives or convex hull shapes from .vtp
    filenames given in a reference file
    """

 
    def __init__(self, ref = 'ref.txt'):
        self._ref = ref
        self._url = list()
        self._attributes = list()
        self._shape = dict()
        self._tri = dict()

        if isinstance(self._ref, str):
            with open(self._ref, 'r') as ref_file:
                for shape_url_line in ref_file:
                    line_tokens = shlex.split(shape_url_line)
                    shape_url = line_tokens[0]
                    shape_attributes = [float(x) for x in (line_tokens[1:])]
                    self._url.append(shape_url)
                    self._attributes.append(shape_attributes)

        # assume hdf5 file
        else:
            acc = []
            for shape_name in self._ref['data']['ref']:
                shape_attributes = self._ref['data']['ref'][shape_name][:]
                shape_id = self._ref['data']['ref'][shape_name].attrs['id']
                if 'url' in self._ref['data']['ref'][shape_name].attrs:
                    shape_url = self._ref['data']['ref'][shape_name].\
                        attrs['url']

                elif 'filename' in self._ref['data']['ref'][shape_name].attrs:
                    shape_url = self._ref['data']['ref'][shape_name].\
                        attrs['filename']

                else:
                    shape_url = self._ref['data']['ref'][shape_name]

                acc.append((shape_attributes, shape_url, shape_id))

            sacc = sorted(acc, key=itemgetter(2))
            self._url = [u for a, u, i in sacc]
            self._attributes = [a for a, u, i in sacc]

        self._primitive = {'Cylinder': btCylinderShape,
                           'Sphere': btSphereShape,
                           'Box': btBoxShape,
                           'Cone': btConeShape,
                           'Compound': btCompoundShape,
                           'Capsule': btCapsuleShape}
        self._primitive = {'Cylinder': 'Cylinder',
                           'Sphere': 'Sphere',
                           'Box': 'Box',
                           'Cone': 'Cone',
                           'Compound': 'Compound',
                           'Capsule': 'Capsule'}

    def at_index(self, index):

        if not index in self._shape:

            # load shape if it is an existing file
            if not isinstance(self._url[index], str) and \
                not 'primitive' in self._url[index].attrs:
                # assume a vtp file (xml) stored in a string buffer
                if self._url[index].dtype == h5py.new_vlen(str):
                    with tmpfile() as tmpf:
                        data = self._url[index][:][0]
                        tmpf[0].write(data)
                        tmpf[0].flush()
                        self._tri[index], self._shape[index] = loadMesh(
                            tmpf[1])
                else:
                    # a convex point set
                    convex = btConvexHullShape()
                    for points in self._url[index]:
                        convex.addPoint(btVector3(float(points[0]),
                                                  float(points[1]),
                                                  float(points[2])))
                    self._shape[index] = convex

            elif isinstance(self._url[index], str) and \
                 os.path.exists(self._url[index]):
                self._tri[index], self._shape[index] = loadMesh(
                    self._url[index])
            else:
                # it must be a primitive with attributes
                if isinstance(self._url[index], str):
                    name = self._url[index]
                    attrs = [float(x) for x in self._attributes[index]]
                else:
                    name = self._url[index].attrs['primitive']
                    attrs = [float(x) for x in self._attributes[index][0]]
                primitive = self._primitive[name]

                if name in ['Box']:
                    self._shape[index] = primitive(btVector3(attrs[0] / 2,
                                                             attrs[1] / 2,
                                                             attrs[2] / 2))
                elif name in ['Cylinder']:
                    self._shape[index] = primitive(btVector3(attrs[0],
                                                             attrs[1] / 2,
                                                             attrs[0]))
                # elif name in ['Compound']:
                #     obj1 = attrs[0]
                #     orig1 = attrs[1:4]
                #     orie1 = attrs[4:8]
                #     obj2 = attrs[8]
                #     orig2 = attrs[9:12]
                #     orie2 = attrs[12:16]
                #     bcols = btCompoundShape()
                #     bcols.addChildShape(...
                else:
                    self._shape[index] = primitive(*attrs)

        return self._shape[index]

    def create_shape(self,io, index):

        #print('isinstance(self._url[index], str', isinstance(self._url[index], str))
        
        if not isinstance(self._url[index], str) and \
           not 'primitive' in self._url[index].attrs:
 
            # assume a vtp file (xml) stored in a string buffer
            if self._url[index].dtype == h5py.new_vlen(str):
                with tmpfile() as tmpf:
                    data = self._url[index][:][0]
                    tmpf[0].write(data)
                    tmpf[0].flush()
                    self._tri[index], self._shape[index] = loadMesh(
                        tmpf[1])
            else:
                # a convex point set
                convex = btConvexHullShape()
                for points in self._url[index]:
                    convex.addPoint(btVector3(float(points[0]),
                                              float(points[1]),
                                              float(points[2])))
                self._shape[index] = convex
            #input()
            
        elif isinstance(self._url[index], str) and \
             os.path.exists(self._url[index]):
            #print('read a vtp file')
            self._tri[index], self._shape[index] = loadMesh(self._url[index])
            
            if isinstance(self._shape[index],btConvexHullShape):
                name = 'ConvexHull'
                points = self._tri[index]
                #print('points', points)
                io.add_convex_shape(name + '_shp_' + str(index),points)
            
            #print('self._tri[index],self._shape[index]', self._tri[index],self._shape[index])
            #input()
            pass
        
        else:
            # it must be a primitive with attributes
            if isinstance(self._url[index], str):
                name = self._url[index]
                attrs = [float(x) for x in self._attributes[index]]
            else:
                name = self._url[index].attrs['primitive']
                attrs = [float(x) for x in self._attributes[index][0]]
            primitive = self._primitive[name]
            
            io.add_primitive_shape(name+ '_shp_' + str(index),primitive,attrs)
            
        return name + '_shp_'  + str(index)

    

class InputData():
    """a Dat context manager reads at instantiation the positions and
       orientations of collision objects from :

       - a ref file (default ref.txt) with shape primitives or shape

         url

       - an input .dat file (default is input.dat)

       input format is :
       shaped_id object_group mass px py pz ow ox oy oz vx vy vx vo1 vo2 vo3

       with
         shape_id : line number in ref file (an integer)
         object group : an integer ; negative means a static object
         mass : mass of the object (a float)
         px py pz : position (float)
         ow ox oy oz : orientation (as an unit quaternion)
         vx vy vx vo1 vo2 vo3 : velocity

       It provides functions to output position and orientation during
       simulation (output is done by default in pos.dat)

       output format is : time object_id px py pz ow ox oy oz

       with:
         time : float
         object_id : the object id (int)
         px, py, pz : components of the position (float)
         ow, ox, oy oz : components of an unit quaternion (float)
    """

    def __init__(self,
                 io,
                 shape_filename='ref.txt',
                 input_filename='input.dat'):
        self._io=io
        self._input_filename = input_filename
        # self._static_origins = []
        # self._static_orientations = []
        # self._static_transforms = []
        # self._static_cobjs = []
        self._shape = ShapeCollection(shape_filename)
        # self._static_pos_file = None
        # self._dynamic_pos_file = None
        # self._contact_forces_file = None
        # self._solver_traces_file = None
        # self._io = MechanicsIO()

        # read data
        with open(self._input_filename, 'r') as input_file:

            with open('bindings.dat', 'w') as bind_file:

                ids = -1
                idd = 1
                for line in input_file:
                    #print('line',line)
                    sline = shlex.split(line)
                    if len(sline) > 3:
                        shape_id = int(sline[0])
                        group_id = int(sline[1])
                        mass = float(sline[2])

                        #print('shape_id, group_is, mass',shape_id, group_id, mass)

                        
                        q0, q1, q2, w, x, y, z, v0, v1, v2, v3, v4, v5 =\
                          [ float(i) for i in sline[3:]]
                        #print('q0, q1, q2, w, x, y, z, v0, v1, v2, v3, v4, v5', q0, q1, q2, w, x, y, z, v0, v1, v2, v3, v4, v5 )
                        if group_id < 0:

                            # add shape 
                            name = self._shape.create_shape(self._io, shape_id)
                            #print('name', name )
                            
                            # add _object
                            self._io.add_object(name+'_bdy_'+str(-ids),
                                                [Contactor(name)],
                                                translation=[q0,q1,q2],
                                                orientation = [w,x,y,z],
                                                velocity=[v0, v1, v2, v3, v4, v5])
                            
                            

                            # # a static object
                            # static_cobj = btCollisionObject()
                            # static_cobj.setCollisionFlags(
                            #     btCollisionObject.CF_STATIC_OBJECT)
                            # origin = btVector3(q0, q1, q2)
                            # self._static_origins.append(origin)
                            # orientation = btQuaternion(x, y, z, w)
                            # self._static_orientations.append(orientation)
                            # transform = btTransform(orientation)
                            # transform.setOrigin(origin)
                            # self._static_transforms.append(transform)
                            # static_cobj.setWorldTransform(transform)
                            # static_cobj.setCollisionShape(
                            #     self._shape.at_index(shape_id))
                            # self._static_cobjs.append(static_cobj)
                            # broadphase.addStaticObject(static_cobj, abs(group_id)-1)
                            # bind_file.write('{0} {1}\n'.format(ids, shape_id))
                            ids -= 1

                        else:
                            # a moving object


                            # add shape 
                            name = self._shape.create_shape(self._io, shape_id)

                            # add _object
                            body=self._io.add_object(name+'_bdy_'+str(idd),
                                                     [Contactor(name)],
                                                     translation=[q0,q1,q2],
                                                     orientation = [w,x,y,z],
                                                     velocity=[v0, v1, v2, v3, v4, v5],
                                                     mass=mass)
                            



                            
                            # body = BulletDS(BulletWeightedShape(
                            #     self._shape.at_index(shape_id), mass),
                            # [q0, q1, q2, w, x, y, z],
                            # [v0, v1, v2, v3, v4, v5])

                            #   # set external forces
                            # set_external_forces(body)

                            # # add the dynamical system to the non smooth
                            # # dynamical system
                            # self._broadphase.model().nonSmoothDynamicalSystem().\
                            # insertDynamicalSystem(body)
                            # self._osi.insertDynamicalSystem(body)
                            bind_file.write('{0} {1}\n'.format(idd, shape_id))
                            idd += 1
                print('Imported objects:')
                print('  number of static objects', ids)
                print('  number of dynamics objects', idd)
                #input()
