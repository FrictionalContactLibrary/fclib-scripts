import os, sys
import shutil as shutil
from glob import glob
import getopt


def usage():
        print(__doc__); print()
        print('Usage: {0} [OPTION]... <HDF5>'
              .format(os.path.split(sys.argv[0])[1]))
        print()


def parse():
    ## Parse command line
    try:
        opts, args = getopt.gnu_getopt(sys.argv[1:], '',
                                    ['help', 'version',
                                     'dat', 'tmin=', 'tmax=',
                                     'no-cf', 'imr', 'global-filter',
                                     'no-depth-peeling',
                                     'maximum-number-of-peels=',
                                     'occlusion-ratio=',
                                     'cf-scale=', 'normalcone-ratio=',
                                     'advance=', 'fps=', 'camera=',
                                     'lookat=',
                                     'up=', 'ortho=', 'visible=', 'with-edges'])
        print('args', args)
        options=[]
        
        if len(args) > 0:
             hdf5_dir= args[0]
        
        for o, a in opts:

            if o == '--help':
                usage(long=True)
                exit(0)

    except getopt.GetoptError as err:
        sys.stderr.write('{0}\n'.format(str(err)))
        usage()
        exit(2)
    return hdf5_dir, options
        

#dir_path = os.path.dirname(os.path.realpath(__file__))
dir_path = os.getcwd()
print('working_dir', dir_path)
hdf5_dir, options = parse()

print('hdf5_dir', hdf5_dir)
if len(sys.argv) > 2:
    print(sys.argv[2])

base = hdf5_dir + '_selected'
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
        
counter =0
max_size = 0

def attributes_split(filename):
    attributes=filename.split('-')
    print(attributes)
    id = int(attributes[-1].split('.')[0])
    print('id', id)
    size = int(attributes[-2])
    print('size',size)
    #iteration = int(attributes[-3][1:])
    #print(iteration)
    return id, size #, iteration


for filename in glob(os.path.join(hdf5_dir+'/*.hdf5')):
    print(filename)
    id, size = attributes_split(filename)
    max_size=max(size,max_size)
    print("max_size", max_size)



n_packets=20
n_files =10
dnp = int(max_size/n_packets)
print("dnp",dnp)

list_filename= []
for i in range(n_packets+1):
    list_filename.append([])

    
for filename in  glob(os.path.join(hdf5_dir+'/*.hdf5')):
    #print( filename)
    id, size = attributes_split(filename)
    print('size/dnp',size/dnp, int(size/dnp))
    #input()
    list_filename[int(size/dnp)-1].append((size,filename))

for i in range(n_packets):
    print('len(list_filename[',i,'])',len(list_filename[i]))
    list_filename[i]= sorted(list_filename[i], key=lambda data: data[0])
    print (list_filename[i][-(n_files+1):-1])
    list_filename[i]=list_filename[i][-(n_files+1):-1]
    print('len(list_filename[',i,'])',len(list_filename[i]))

    for size_f,f in  list_filename[i]:
        print(size_f,f)
        new_filename = f.split('/')[-1]
        print("copy", f, "in ", os.path.join(output_dir, new_filename))
        shutil.copy(f, os.path.join(output_dir, new_filename))
    #statinfo = os.stat(os.path.join(dirname, filename))
    #print statinfo.st_size,  statinfo_previous.st_size
    #new_filename = filename.replace('FC3D',base)
    # if counter%1==0 :
    #     print "copy", filename, "in ", os.path.join(base, new_filename) 
    #     shutil.copy(filename, os.path.join(base, new_filename))
    # counter =counter +1
