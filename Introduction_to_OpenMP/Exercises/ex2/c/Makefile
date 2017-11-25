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
LDFLAGS=-L/group/courses01/ADACS_workshop_2017/lib/gcc/5.4.0 -lmap-sampler-pmpi -lmap-sampler -Wl,--eh-frame-hdr -Wl,-rpath=/group/courses01/ADACS_workshop_2017/lib/gcc/5.4.0
 

all:
	$(CC) $(CFLAGS) pi-serial.c -o pi-serial 
	$(MPICC) $(CFLAGS) pi-serial.c -o pi-serial-prof $(LDFLAGS)
clean:
	rm -rf pi-serial pi-serial-prof
