
/******************************************************************************
 *
 *   Pass a message around a ring in one dimension with the aid of a
 *   periodic Cartesian communicator.
 *  
 *   We use synchronous non-blocking communications and mpi_waitall()
 *   to pass the message
 *
 ******************************************************************************/

#include <mpi.h>
#include <stdio.h>

int main (int argc, char* argv[]){

  int i, rank, size;
  int sum;

  /* 1-d Cartesian communicator */
  MPI_Comm comm;
  int my_left, my_right;
  int ndims = 1;
  int dims[1];
  int periods[1];

  /* Message information */
  int sendbuf, recvbuf;
  int my_tag = 9999;
  MPI_Request req[2];
  MPI_Status status[2];

  /* loop counter */
  int n;

  MPI_Init(&argc,&argv);
	
  MPI_Comm_rank(MPI_COMM_WORLD,&rank);
  MPI_Comm_size(MPI_COMM_WORLD,&size);

  /*  Create periodic Cartesian communicator
   *   The 'reorder' parameter is set to .true., meaning MPI is allowed to
   *   reorder the ranks in the new communicator */
  periods[0] = 1; 
  dims[0] = size;

  MPI_Dims_create(size, ndims, dims);
  MPI_Cart_create(MPI_COMM_WORLD, ndims, dims, periods, 1, &comm);         

  /* check rank in new communicator
   * and work out neighbouring ranks in 1-d: my_left - rank - my_right */

  MPI_Comm_rank(comm, &rank);
  MPI_Cart_shift(comm, 0, 1, &my_left, &my_right);

  /* Initialise the sum and the message for all ranks */
  sum = 0;
  sendbuf = rank;

  for(i = 0; i < size; i++){
  	MPI_Irecv(&recvbuf, 1, MPI_INT, my_left, my_tag, comm, req); 
  	MPI_Issend(&sendbuf, 1, MPI_INT, my_right, my_tag, comm, req+1);
  	MPI_Waitall(2, req, status);

  	sum = sum + recvbuf;
  	sendbuf = recvbuf;
  }

  /* Display the result on all ranks, along with the correct answer */
  printf("Rank %2d has sum of ranks %d; Answer %d \n", rank, sum, (size-1)*size/2);

  MPI_Finalize();
	
  return 0;

} 
