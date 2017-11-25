ifeq ($(CRAYOS_VERSION),)
	CC=gcc
	F90=gfortran
else
	CC=cc
	F90=ftn
endif


OMP_FLAG=-fopenmp
CFLAGS=-g $(OMP_FLAG)
 

all:
	$(CC) $(CFLAGS) hello-omp.c -o hello-omp 
clean:
	rm -rf hello-omp
