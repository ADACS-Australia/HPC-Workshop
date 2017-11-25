ifeq ($(CRAYOS_VERSION),)
	MPIF90=mpicc
	MPIF90=mpif90
else
	MPIF90=cc
	MPIF90=ftn
endif


FFLAGS=-g 
LDFLAGS=-L/group/courses01/ADACS_workshop_2017/lib/gcc/5.4.0 -lmap-sampler-pmpi -lmap-sampler -Wl,--eh-frame-hdr -Wl,-rpath=/group/courses01/ADACS_workshop_2017/lib/gcc/5.4.0

all:
	$(MPIF90) $(FFLAGS) life-serial.f90 -o life-serial
	$(MPIF90) $(FFLAGS) life-serial.f90 -o life-serial-prof $(LDFLAGS)

clean:
	rm -rf life-serial life-serial-prof
