import os
import shutil as shutil
from glob import glob 

rename=False
base = './PrimitiveSoup_selected'
source_dir='./PrimitiveSoup_0/'

base = './Capsules_selected'
source_dir='./Capsules_0/'

#base = './Chute_selected'
#source_dir='./Chute_0/'

base = './Spheres_selected'
source_dir='./Spheres_0/'

base = './KaplasTower_selected'
source_dir='./KaplasTower_0/'

rename=True
new_name='Spheres1mmScaled'
base = './Spheres_1mm_selected'
source_dir='./Spheres_0/'



os.mkdir(base)
counter =0
max_size = 0
min_size = 10000000000
def attributes_split(filename):
    attributes=filename.split('-')
    #print('attributes:',attributes)
    id = int(attributes[-1].split('.')[0])
    #print('id:',id)
    size = int(attributes[-2])
    #print('size:',size)
    ndof = int(attributes[-4])
    #print('ndof:', ndof)
    return id, size, ndof


def select_the_largest_ones_in_packet(list_filename,  n):
    print('\nselect_the_largest_ones_in_packet')
    nb_files = len(list_filename)
    print('number of files in packet', nb_files)

    list_filename= sorted(list_filename, key=lambda data: data[0])

    selected_filename = list_filename[-(n+1):-1]
    print('number of files of selected file', len(selected_filename))
    print('selected files:', selected_filename)

    return selected_filename

import random



def select_randomly_in_packet(list_filename,  n):
    print('\nselect_randomly_in_packet')
    nb_files = len(list_filename)
    print('number of files in packet', nb_files)
    list_filename= sorted(list_filename, key=lambda data: data[0])
    #print('sorted files',list_filename)
    
    min_size= list_filename[0][0]
    max_size= list_filename[-1][0]
    print('min size:', min_size, 'maz_size:', max_size, 'in the packet')

    sizes = set()

    for f in list_filename:
        sizes.add(f[0])
    print('sizes', sizes, len(sizes))

    files_by_size = {}
    for s in sizes:
        files_by_size[s] = []
        
    for f in list_filename:
        files_by_size[f[0]].append(f)

    #print('files_by_size', files_by_size)


    n_max =  min(n,len(list(sizes)))


    print("randomly select", n_max , "sizes in list_sizes of len ", len(list(sizes)) )


    
    
    selected_sizes=random.sample(list(sizes), n_max )
    print('selected_sizes', selected_sizes, len(selected_sizes))

    selected_filename = []
    
    for ss in selected_sizes:
        selected_filename.append(files_by_size[ss][0])
    
    print('number of files of selected file', len(selected_filename))
    print('selected files:', selected_filename)

    return selected_filename






# compute max size (max number of contact)
for filename in glob(source_dir+'*.hdf5'):
    #print( filename)
    id, size, ndof = attributes_split(filename)
    max_size=max(size,max_size)
    min_size=min(size,min_size)

print("max_size:", max_size)
print("min_size:", min_size)

# compute packets of sizes
# Classify files w.r.t to the size in packet
# this is done by computing the ratio between size and dnp
# and taking the int floor value
    
n_packets=10
n_files =30
dnp = max_size/n_packets
print("dnp",dnp)

import numpy as np

list_filename= []
for i in range(n_packets):
    list_filename.append([])

# packets_sizes =[]
# for i in range(n_packets):
#     packets_sizes.append([])

# for i in range(max_size):
#     packets_sizes[int((i)/dnp)-1].append(i)

# for p in packets_sizes:
#     print('packets min max', np.min(np.array(p)), np.max(np.array(p)))

    
# #print('packets_sizes', packets_sizes)
# input()


## creation of packets by size
for filename in glob(source_dir+'*.hdf5'):
    #print( filename)
    id, size, ndof = attributes_split(filename)
    print(filename, 'of size', size, 'in packet number size/dnp-1',int((size)/dnp)-1)
    list_filename[int((size)/dnp)-1].append((size,filename))


number_selected_files=0
# select the files in each packets by keeping the largest one or randomly selected in packets
for i in range(n_packets):
    # selection in packet
    #list_filename[i] = select_the_largest_ones_in_packet(list_filename[i],  n_files)
    if len(list_filename[i])>0: 
        list_filename[i] = select_randomly_in_packet(list_filename[i],  n_files)
        #input()
        # copy in destination dir
        for size_f,f in  list_filename[i]:
            print(size_f,f)
            new_filename = f.split('/')[-1]
            print("copy", f, "in ", os.path.join(base, new_filename))
            shutil.copy(f, os.path.join(base, new_filename))
            number_selected_files=number_selected_files + 1

print('number of selected files', number_selected_files)
        

if rename:
    print(base+'/*.hdf5')
    for filename in glob(base+'/*.hdf5'):
        print(filename, os.path.basename(filename))
        basename_l = os.path.basename(filename).split('-')
        print(basename_l)
        
        basename_l[0]=new_name
        new_filename='-'.join(basename_l)
        print(new_filename)
        print("mv", filename, "in ", os.path.join(base, new_filename))
        shutil.move(filename, os.path.join(base, new_filename))
