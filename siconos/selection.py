import os
import shutil as shutil
from glob import glob 
base = './PrimitiveSoup_selected'
source_dir='./PrimitiveSoup_0/'
base = './Capsules_selected'
source_dir='./Capsules_0/'
#base = './Chute_selected'
#source_dir='./Chute_0/'
os.mkdir(base)
counter =0
max_size = 0

def attributes_split(filename):
    attributes=filename.split('-')
    print('attributes:',attributes)
    id = int(attributes[-1].split('.')[0])
    print('id:',id)
    size = int(attributes[-2])
    print('size:',size)
    ndof = int(attributes[-4])
    print('ndof:', ndof)
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
    print( filename)
    id, size, ndof = attributes_split(filename)
    max_size=max(size,max_size)
    print("max_size:", max_size)

# compute packets of sizes
# Classify files w.r.t to the size in packet
# this is done by computing the ratio between size and dnp
# and taking the int floor value
    
n_packets=10
n_files =20
dnp = max_size/n_packets
print("dnp",dnp)

list_filename= []
for i in range(n_packets):
    list_filename.append([])

for filename in glob(source_dir+'*.hdf5'):
    #print( filename)
    id, size, ndof = attributes_split(filename)
    print('in packet number size/dnp-1',int((size)/dnp)-1)
    list_filename[int((size)/dnp)-1].append((size,filename))


number_selected_files=0
# select the files in each packets by keeping the largest one or randomly selected in packets
for i in range(n_packets):
    # selection in packet
    #list_filename[i] = select_the_largest_ones_in_packet(list_filename[i],  n_files)
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


        
