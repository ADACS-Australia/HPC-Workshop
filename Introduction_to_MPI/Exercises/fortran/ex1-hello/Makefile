ifeq ($(CRAYOS_VERSION),)
	MPICC=mpicc
	MPIF90=mpif90
else
	MPICC=cc
	MPIF90=ftn
endif


FFLAGS=-g 
 

all:
	$(MPIF90) $(FFLAGS) hello.f90 -o hello-mpi 
clean:
	rm -rf hello-mpi
