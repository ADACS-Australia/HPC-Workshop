ifeq ($(CRAYOS_VERSION),)
	CC=mpicc
	F90=mpif90
else
	CC=cc
	F90=ftn
endif

all:
	$(CC) src/matrix-generator.c -o matrix-generator

clean:
	rm matrix-generator 
