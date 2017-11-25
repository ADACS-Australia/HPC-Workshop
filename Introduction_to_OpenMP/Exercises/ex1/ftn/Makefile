ifeq ($(CRAYOS_VERSION),)
	CC=gcc
	F90=gfortran
else
	CC=cc
	F90=ftn
endif


OMP_FLAG=-fopenmp
FFLAGS=-g $(OMP_FLAG)
 

all:
	$(F90) $(FFLAGS) hello-omp.f90 -o hello-omp 
clean:
	rm -rf hello-omp
