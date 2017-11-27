ifeq ($(CRAYOS_VERSION),)
	CC=gcc
	F90=gfortran
	MPICC=mpicc
	MPIF90=mpif90
else
	CC=cc
	F90=ftn
endif


CFLAGS=-g -fopenmp
 

all:
	$(CC) $(CFLAGS) pi-omp-v1.c -o pi-omp-v1 
clean:
	rm -rf pi-omp-v1
