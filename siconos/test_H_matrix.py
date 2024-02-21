import h5py
from scipy.sparse import coo_matrix
#filename = 'Global/siconos/PrimitiveSoup/PrimitiveSoup-i080-247-7.hdf5'


mypath = 'Global/siconos/Spheres/'
mypath = 'Global/Spheres_1mm/'
mypath='/scratch/vincent/fclib-library/Global/siconos/Spheres/'
mypath='/scratch/vincent/fclib-library/Global/siconos/Chute/'
import numpy as np

def test_H_ONB(filename, key):

    f = h5py.File(filename,'r')
    #print('test size for ', key)
    # print(f.keys())
    if not ('fclib_global' in f.keys()):
        return False
        
    
    #print(f['fclib_global'][key].keys())
    nz = f['fclib_global'][key]['nz'][0]
    m = f['fclib_global'][key]['m'][0]
    n = f['fclib_global'][key]['n'][0]
    
    # print('nz',nz)
    # print('m',m)
    # print('n',n)
    nzmax = f['fclib_global'][key]['nzmax'][0]
    # print('nzmax',nzmax)
    x = f['fclib_global'][key]['x'][:]
    idx = f['fclib_global'][key]['i'][:]
    jdx = f['fclib_global'][key]['p'][:]

    H = coo_matrix((x, (idx, jdx)), shape=(m,n) ).toarray().transpose()
    #print(H, H.shape)

    # find block
    max_error =0.
    #print(filename)
    for i in np.arange(0,n,3):
        #print(i, H.data[i])
        for j in np.arange(0,m,6):
            
            block=np.zeros((3,6))
            block[:,:] = H[i:i+3,j:j+6]
            if np.linalg.norm(block) > 1e-100:
                # test
                n = block[:,0]
                t = block[:,1]
                s = block[:,2]

                ok =True
                tol =1e-04

                print('norm n',np.linalg.norm(n))
                print('norm t',np.linalg.norm(t))
                print('norm s',np.linalg.norm(s))
                
                print('n.s',np.dot(n,s))
                print('n.t',np.dot(n,t))
                print('s.t',np.dot(s,t))
                
                error = max(np.dot(n,s),np.dot(t,s))
                error = max(error,np.dot(n,t))
                max_error = max(error,max_error)
                if error > tol:
                    ok = False
                # if not ok:
                #     print(block)


                #     print(i,j)
                #     print(block)
                #     print('norm n',np.linalg.norm(n))
                #     print('norm t',np.linalg.norm(t))
                #     print('norm s',np.linalg.norm(s))
                
                #     print('n.s',np.dot(n,s))
                #     print('n.t',np.dot(n,t))
                #     print('s.t',np.dot(s,t))
                    #input()
                # if not ok:
                #     return False
    print('max_error', max_error)
    #assert(idx.shape[0] == nz)
    #assert(jdx.shape[0] == nz)
    #assert(x.shape[0] == nz)
    return ok
 
def test_w_in_range_of_H(filename, key):

    f = h5py.File(filename,'r')
    #print('test size for ', key)
    # print(f.keys())
    if not ('fclib_global' in f.keys()):
        return False
        
    
    #print(f['fclib_global'][key].keys())
    nz = f['fclib_global'][key]['nz'][0]
    m = f['fclib_global'][key]['m'][0]
    n = f['fclib_global'][key]['n'][0]
    
    # print('nz',nz)
    # print('m',m)
    # print('n',n)
    nzmax = f['fclib_global'][key]['nzmax'][0]
    # print('nzmax',nzmax)
    x = f['fclib_global'][key]['x'][:]
    idx = f['fclib_global'][key]['i'][:]
    jdx = f['fclib_global'][key]['p'][:]

    H = coo_matrix((x, (idx, jdx)), shape=(m,n) ).toarray().transpose()
    #print(H, H.shape)

    
    w = f['fclib_global']['vectors']['w'][:]
    if np.linalg.norm(w) > 1e-10:
        print(np.linalg.norm(w))

    else:
        print('w is null')
        return True

    #HHT = np.dot(H,H.T)
    #print(HHT)
    
        
    
    return True
 
    
import os
from os import walk

test = []

for (dirpath, dirnames, filenames) in walk(mypath):
    print(dirpath, dirnames, filenames)

    for f in filenames:
        if 'Rolling' in f or 'Rolling' in dirpath:
            break
        ext = os.path.splitext(f)[-1].lower()
        if ext == ".hdf5":
            print('\nfilename', os.path.join(dirpath,f))
            #test_size(os.path.join(dirpath,f), 'M')
            #ok = test_H_ONB(os.path.join(dirpath,f), 'H')
            ok = test_w_in_range_of_H(os.path.join(dirpath,f), 'H')
            if not ok:
                test.append(os.path.join(dirpath,f))


print(test)

