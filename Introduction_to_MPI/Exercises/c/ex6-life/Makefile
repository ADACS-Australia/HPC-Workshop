ifeq ($(CRAYOS_VERSION),)
	MPICC=mpicc
	MPIF90=mpif90
else
	MPICC=cc
	MPIF90=ftn
endif


CFLAGS=-g 
LDFLAGS=-L/group/courses01/ADACS_workshop_2017/lib/gcc/5.4.0 -lmap-sampler-pmpi -lmap-sampler -Wl,--eh-frame-hdr -Wl,-rpath=/group/courses01/ADACS_workshop_2017/lib/gcc/5.4.0

all:
	$(MPICC) $(CFLAGS) life-serial.c -o life-serial
	$(MPICC) $(CFLAGS) life-serial.c -o life-serial-prof $(LDFLAGS)

clean:
	rm -rf life-serial life-serial-prof
