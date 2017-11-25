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
CFLAGS=-g $(OMP_FLAG)


all: hello serial omp-v1 omp-v2

hello:
	$(CC) $(CFLAGS) $(SOURCE)/hello-omp.c -o hello-omp 
serial:
	$(CC) $(CFLAGS) $(SOURCE)/pi-serial.c -o pi-serial 
omp-v1:
	$(CC) $(CFLAGS) $(SOURCE)/pi-omp-v1.c -o pi-omp-v1 
omp-v2: 
	$(CC) $(CFLAGS) $(SOURCE)/pi-omp-v2.c -o pi-omp-v2 
clean:
	rm -rf hello-omp pi-serial pi-omp-v1 pi-omp-v2
