
/******************************************************************************
 *
 * Accumulate the sum of the ranks by sending a message around a
 * ring.
 *
 *  We use a synchronous non-blocking send mpi_issend() and a non-
 *  blocking recieve mpi_irecv(), along with two wait statements.
 *
 *****************************************************************************/

#include <mpi.h>
#include <stdio.h>

int main (int argc, char* argv[]){

  int rank, size;
  int my_prev, my_next;
  int sum;

  /*  Message information  */
  int sendbuf, recvbuf;
  int my_tag = 9999;
  MPI_Request reqr;
  MPI_Request reqs;
  MPI_Status status[1];

  /* loop counter */
  int n;

  MPI_Init(&argc,&argv);

  MPI_Comm_rank(MPI_COMM_WORLD, &rank);
  MPI_Comm_size(MPI_COMM_WORLD, &size);

  /* Work out neighbouring ranks */
  my_prev = rank - 1;
  
  if (my_prev < 0) 
  	my_prev = my_prev + size;
  
  my_next = (rank + 1) % size;

  /* Initialise the sum and the message for all ranks */
  sum = 0;
  sendbuf = rank;
        
  for (n = 0; n < size; n++) {
    MPI_Irecv(&recvbuf, 1, MPI_INT, my_prev, my_tag, MPI_COMM_WORLD, &reqr);
    MPI_Issend(&sendbuf, 1, MPI_INT, my_next, my_tag, MPI_COMM_WORLD, &reqs);

    /* When the receive has completed, we can use the contents of recvbuf */
    MPI_Wait(&reqr, status);
    sum = sum + recvbuf;

    /* When the send has completed, we can safely re-use the send buffer */
    MPI_Wait(&reqs, status);
    sendbuf = recvbuf;
  }

  /* Display the result on all ranks, along with the correct answer */

  printf("Rank %2d has sum of ranks %d; Answer = %d\n",rank, sum, (size-1)*size/2);

  MPI_Finalize();
	
  return 0;

} 
