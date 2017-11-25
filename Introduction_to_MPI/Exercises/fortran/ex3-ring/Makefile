ifeq ($(CRAYOS_VERSION),)
	MPIF90=mpicc
	MPIF90=mpif90
else
	MPIF90=cc
	MPIF90=ftn
endif


FFLAGS=-g 
 

all:
	$(MPIF90) $(FFLAGS) ring.f90 -o ring
clean:
	rm -rf ring
