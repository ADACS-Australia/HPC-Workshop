ifeq ($(CRAYOS_VERSION),)
	MPICC=mpicc
	MPIF90=mpif90
else
	MPICC=cc
	MPIF90=ftn
endif


FFLAGS=-g 
 

all:
	$(MPIF90) $(FFLAGS) pingpong.f90 -o pingpong
clean:
	rm -rf pingpong
