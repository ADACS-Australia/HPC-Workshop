#include <mpi.h>
#include <stdio.h>

/* Ring program */

int main (int argc, char* argv[]){

  int rank, size;
  int sum = 0;

  /* ... */

  MPI_Init(&argc,&argv);

  MPI_Comm_rank(MPI_COMM_WORLD, &rank);
  MPI_Comm_size(MPI_COMM_WORLD, &size);

  /* Work out neighbouring ranks */
  /*... */

  /* Initialise the sum */
  /* ... */

  /* Send messages */
  /* ... */

  /* Display the result on all ranks, along with the correct answer */

   printf("Rank %2d has sum of ranks %d; Answer = %d\n",rank, sum, (size-1)*size/2);
  
  MPI_Finalize();

  return 0;

} 
