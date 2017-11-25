ifeq ($(CRAYOS_VERSION),)
	MPICC=mpicc
	MPIF90=mpif90
else
	MPICC=cc
	MPIF90=ftn
endif


CFLAGS=-g 
 

all:
	$(MPICC) $(CFLAGS) ring.c -o ring
clean:
	rm -rf ring
