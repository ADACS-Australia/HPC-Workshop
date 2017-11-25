CC=cc
F90=ftn
PRGENV=${PE_ENV}
FFLAGS=-g
SOURCE=pi-omp-v1.f90
OBJ=pi-omp-v1.o
EXE=pi-omp-v1.out

ifeq ($(PRGENV),INTEL)
	OMP_FLAG=-openmp
else ifeq ($(PRGENV),GNU)
	OMP_FLAG=-fopenmp
else ifeq ($(PRGENV),CRAY)
	OMP_FLAG=-homp
endif 


%.o: %.f90
	$(F90) -c -o $@ $< $(FFLAGS) $(OMP_FLAG)
pi-omp-v1: $(OBJ)
	$(F90) $(FFLAGS) $(OBJ) -o $(EXE) $(OMP_FLAG)

clean:
	rm -rf $(EXE) $(OBJ)
