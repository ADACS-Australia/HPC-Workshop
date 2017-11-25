ifeq ($(CRAYOS_VERSION),)
	MPICC=mpicc
	MPIF90=mpif90
else
	MPICC=cc
	MPIF90=ftn
endif

CFLAGS = -g -std=gnu99 $(OMP_FLAGS)


SOURCE = src
INC= -I ./include
LDFLAGS=-L/group/courses01/ADACS_workshop_2017/lib/gcc/5.4.0 -lmap-sampler-pmpi -lmap-sampler -Wl,--eh-frame-hdr -Wl,-rpath=/group/courses01/ADACS_workshop_2017/lib/gcc/5.4.0

all: mpi_latency mpi_bandwidth_blocking mpi_bandwidth_nonblocking gaussian_serial gaussian_mpi cart_shift dims_test

mpi_latency: 
	$(MPICC) $(CFLAGS) $(SOURCE)/mpi_latency.c -o latency
mpi_bandwidth_blocking:
	$(MPICC) $(CFLAGS) $(SOURCE)/mpi_bandwidth.c -o bandwidth-blocking
mpi_bandwidth_nonblocking:
	$(MPICC) $(CFLAGS) $(SOURCE)/mpi_bandwidth-nonblock.c -o bandwidth-nonblocking

gaussian_mpi: 
	$(MPICC) $(CFLAGS) $(SOURCE)/gaussian-mpi-version.c $(SOURCE)/gauss-main-mpi.c -o gauss-mpi $(INC) $(LDFLAGS) 
	$(MPICC) $(CFLAGS) -DPARALLEL_IO $(SOURCE)/gaussian-mpi-version.c $(SOURCE)/gauss-main-mpi.c -o gauss-mpi-pario $(INC) $(LDFLAGS) 

gaussian_serial: 
	$(CC) $(CFLAGS) $(SOURCE)/gaussian-serial-version.c $(SOURCE)/gauss-main-serial.c -o gauss-serial $(INC) $(LDFLAGS)
cart_shift:
	$(MPICC) $(CFLAGS) cart_shift.c -o cart_shift
dims_test:
	$(MPICC) $(CFLAGS) dims_test.c -o dims_test

clean:
	rm -r latency bandwidth-blocking bandwidth-nonblocking gauss-serial gauss-mpi cart_shift dims_test gauss-mpi-pario

