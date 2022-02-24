
# Generation of examples for siconos

## Local example

### old style

For instance in Kaplas

cd Local/Kaplas
- generation of the file input.dat and bindings.dat using the shape in ref.txt
  python mkinput.py

- execution of the running script
  python ../run.py

Most of the example in fclib-library tag v1.0 have been generated in that way


### new style

For instance in Capsules

cd Local/Capsule
- generation of the file input.dat and bindings.dat using the shape in ref.txt
  python mkinput.py

- execution of the running script
  python python capsules_with_trace.py


  





## Global example

For instance in Global/Spheres

- generation of the file input.dat and bindings.dat using the shape in ref.txt
  python mkinput.py

- execution of the running script
  python spheres_with_trace_global.py

- selection of a part of the generated file
  python ../../selection.py Spheres_0
  	    

