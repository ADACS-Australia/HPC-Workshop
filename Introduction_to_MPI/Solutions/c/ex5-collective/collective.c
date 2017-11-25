#include <mpi.h>
#include <stdio.h>

int main (int argc, char* argv[]){

  int rank, size;
  int sum;

  MPI_Init(&argc,&argv);
	
  MPI_Comm_rank(MPI_COMM_WORLD, &rank);
  MPI_Comm_size(MPI_COMM_WORLD, &size);

  MPI_Allreduce(&rank, &sum, 1, MPI_INT, MPI_SUM, MPI_COMM_WORLD);

  /* Display the result on all ranks, along with the correct answer */
  printf("Rank %2d has sum of ranks %d; Answer %d \n", rank, sum, (size-1)*size/2);

  MPI_Finalize();
	
  return 0;

} 
