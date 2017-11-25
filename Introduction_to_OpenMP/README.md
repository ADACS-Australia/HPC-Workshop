# Develop-with-OpenMP
Exercises for the OpenMP develop course
The input data for the demo can be created using the matrix_generator. 
matrix_generator is an MPI application and can be invoked as follows for e.g. 4 MPI tasks:

srun -n 4 --export=all matrix_generator 256

This will generate an augmented matrix of size 256 x 257 writing binary data of type float. 

Each Exercise directory contains the C or Fortran version, a Makefile and jobscript to submit the job to 
the reservation on Athena gpuq partition. 
The Solution directory has solution to all the exercises, along with a Makefile and a jobscript template. 


