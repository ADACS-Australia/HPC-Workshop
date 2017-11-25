ifeq ($(CRAYOS_VERSION),)
	CC=gcc
	F90=gfortran
	MPICC=mpicc
	MPIF90=mpif90
else
	CC=cc
	F90=ftn
endif

SOURCE=src
INC=-I./include

CFLAGS=-g
#LDFLAGS=-L/group/courses01/ADACS_workshop_2017/lib/gcc/5.4.0 -lmap-sampler-pmpi -lmap-sampler -Wl,--eh-frame-hdr -Wl,-rpath=/group/courses01/ADACS_workshop_2017/lib/gcc/5.4.0
 

all:
	$(CC) $(CFLAGS) $(SOURCE)/gaussian-serial-version.c  $(SOURCE)/gauss-main-serial.c -o gauss-serial $(INC) $(LDFLAGS)
clean:
	rm -rf gauss-serial
