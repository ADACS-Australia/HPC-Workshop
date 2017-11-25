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
SOURCE=src
OMP_FLAG=-fopenmp
FFLAGS=-g $(OMP_FLAG) -fno-range-check


all: hello serial omp-v1 omp-v2

hello:
	$(FC) $(FFLAGS) $(SOURCE)/hello-omp.f90 -o hello-omp 
serial:
	$(FC) $(FFLAGS) $(SOURCE)/pi-serial.f90 -o pi-serial
omp-v1:
	$(FC) $(FFLAGS) $(SOURCE)/pi-omp-v1.f90 -o pi-omp-v1
omp-v2: 
	$(FC) $(FFLAGS) $(SOURCE)/pi-omp-v2.f90 -o pi-omp-v2
clean:
	rm -rf hello-omp pi-serial pi-omp-v1 pi-omp-v2
