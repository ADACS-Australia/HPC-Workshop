#include <mpi.h>
#include <stdio.h>

/* Pingpong program */

int main (int argc, char* argv[]){

  int rank, size;

  /* ... */
	
  MPI_Init(&argc,&argv);

  MPI_Comm_rank(MPI_COMM_WORLD,&rank);
  MPI_Comm_size(MPI_COMM_WORLD,&size);

  if (size != 2){
  	printf("Must use exactly two MPI tasks\n");
        MPI_Abort(MPI_COMM_WORLD, 1);
  }

  /* ... */
  /* ... */

  MPI_Finalize();
  
  return 0;

} 
