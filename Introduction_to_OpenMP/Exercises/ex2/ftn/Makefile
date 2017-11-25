ifeq ($(CRAYOS_VERSION),)
	CC=gcc
	F90=gfortran
	MPICC=mpicc
	MPIF90=mpif90
else
	CC=cc
	F90=ftn
endif


FFLAGS=-g -fopenmp -fno-range-check
LDFLAGS=-L/group/courses01/ADACS_workshop_2017/lib/gcc/5.4.0 -lmap-sampler-pmpi -lmap-sampler -Wl,--eh-frame-hdr -Wl,-rpath=/group/courses01/ADACS_workshop_2017/lib/gcc/5.4.0
 

all:
	$(F90) $(FFLAGS) pi-serial.f90 -o pi-serial 
	$(MPIF90) $(FFLAGS) pi-serial.f90 -o pi-serial-prof $(LDFLAGS)
clean:
	rm -rf pi-serial pi-serial-prof
