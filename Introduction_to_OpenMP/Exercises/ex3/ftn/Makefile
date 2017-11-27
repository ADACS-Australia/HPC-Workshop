ifeq ($(CRAYOS_VERSION),)
	CC=gcc
	MPICC=mpicc
	F90=gfortran
	MPIF90=mpif90
else
	CC=cc
	F90=ftn
	MPICC=cc
	MPIF90=ftn
endif
OMP_FLAG=-fopenmp
FFLAGS=-g $(OMP_FLAG) -fno-range-check


all: pi-omp-v1

pi-omp-v1:
	$(FC) $(FFLAGS) pi-omp-v1.f90 -o pi-omp-v1
clean:
	rm -rf  pi-omp-v1
