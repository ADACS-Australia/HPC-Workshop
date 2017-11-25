CC=cc
F90=ftn
PRGENV=${PE_ENV}
CFLAGS=-g
SOURCE=pi-omp-v1.c
OBJ=pi-omp-v1.o
EXE=pi-omp-v1.out

ifeq ($(PRGENV),INTEL)
	OMP_FLAG=-openmp
else ifeq ($(PRGENV),GNU)
	OMP_FLAG=-fopenmp
else ifeq ($(PRGENV),CRAY)
	OMP_FLAG=-homp
endif 


%.o: %.c 
	$(CC) -c -o $@ $< $(CFLAGS) $(OMP_FLAG)
pi-omp-v1: $(OBJ)
	$(CC) $(CFLAGS) $(OBJ) -o $(EXE) $(OMP_FLAG)

clean:
	rm -rf $(EXE) $(OBJ)
