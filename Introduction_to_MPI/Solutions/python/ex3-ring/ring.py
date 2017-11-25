##########################################################################
## 
##  An MPI program where we accumulate the sum of all active MPI ranks by 
##  sending a message around a ring.
##
##  We use a synchronous non-blocking send mpi_issend() and a non-blocking
##  recieve mpi_irecv(), along with two wait statements.
##########################################################################


from mpi4py import MPI
import numpy as np

comm = MPI.COMM_WORLD
rank = comm.Get_rank()
size = comm.Get_size()

# Work out neighbouring ranks

my_prev = rank - 1
if ( my_prev < 0 ):
   my_prev += size

my_next = (rank + 1) % size

# Initialise the sum value 
sum = 0

# Set the size and datatype for the send and receive message buffers
sendbuf = np.empty( [1], dtype=np.int )
sendbuf[0] = rank
recvbuf = np.empty( [1], dtype=np.int )

for i in range(size):
    reqr = comm.irecv( source=my_prev, tag=9999 )
    reqs = comm.isend( [sendbuf, MPI.INT], dest=my_next, tag=9999 )

  # When the receive has completed, we can use the contents of recvbuf
    recvbuf = reqr.wait()
    sum += recvbuf[0]

  # When the send has completed, we can safely re-use the send buffer
    reqs.wait()
    sendbuf[0] = recvbuf[0]

# Display the result on all ranks, along with the correct answer
print "Rank " + str(rank) + " has sum of ranks " + str(sum) + "; Answer = " + str( (size-1)*size/2 )

