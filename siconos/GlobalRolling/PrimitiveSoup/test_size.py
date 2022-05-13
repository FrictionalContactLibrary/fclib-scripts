import h5py

#filename = 'Global/siconos/PrimitiveSoup/PrimitiveSoup-i080-247-7.hdf5'
mypath = 'Global/siconos/PrimitiveSoup/'

#mypath = 'Global/siconos/KaplasTower/'
#mypath = 'Global/siconos/Spheres/'
#mypath = 'Global/siconos/Chute/'
#mypath = 'Global/siconos/Spheres1mm/'
mypath = 'PrimitiveSoup_0'


import numpy as np

def test_size(filename, key):

    f = h5py.File(filename,'r')
    print('test size for ', key)
    
    print(f['fclib_global'][key].keys())

    nz = f['fclib_global'][key]['nz'][0]
    m = f['fclib_global'][key]['m'][0]
    n = f['fclib_global'][key]['n'][0]
    print('nz',nz)
    print('m',m)
    print('n',n)
    nzmax = f['fclib_global'][key]['nzmax'][0]
    print('nzmax',nzmax)
    x = f['fclib_global'][key]['x'][:]
    idx = f['fclib_global'][key]['i'][:]
    jdx = f['fclib_global'][key]['p'][:]
    # print('x',x)
    # for i in range(nz,nzmax):
    #     print('x[i]',x[i])
    #     print('idx[i]',idx[i])
    #     input()
    print('norm', np.linalg.norm(x[nz:nzmax]))
    print('norm of the last tens', np.linalg.norm(x[nz-10:nz]))
    print('x.shape[0]',x.shape[0])
    print('idx.shape[0]', idx.shape[0])
    print('jdx.shape[0]', jdx.shape[0])

    assert(idx.shape[0] == nz)
    assert(jdx.shape[0] == nz)
    assert(x.shape[0] == nz)
 

    
import os
from os import walk


for (dirpath, dirnames, filenames) in walk(mypath):
    print(dirpath, dirnames, filenames)

    for f in filenames:
        
        ext = os.path.splitext(f)[-1].lower()
        if ext == ".hdf5":
            print('\nfilename', os.path.join(dirpath,f))
            test_size(os.path.join(dirpath,f), 'M')
            test_size(os.path.join(dirpath,f), 'H')


