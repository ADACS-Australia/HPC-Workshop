ifeq ($(CRAYOS_VERSION),)
	MPICC=mpicc
	MPIF90=mpif90
else
	MPICC=cc
	MPIF90=ftn
endif


CFLAGS=-g 
 

all: simple_write simple_read strided_read

simple_write: 
	$(MPICC) $(CFLAGS) simple_write.c -o simple_write
simple_read:
	$(MPICC) $(CFLAGS) simple_read.c -o simple_read
strided_read:
	$(MPICC) $(CFLAGS) strided_read.c -o strided_read
clean:
	rm -rf simple_read strided_read simple_write 
