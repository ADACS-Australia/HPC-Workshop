########################################################################
##    Pass a message around a ring in one dimension with the aid of a
##    periodic Cartesian communicator.
##   
##    We use synchronous non-blocking communications and mpi_waitall()
##    to pass the message
########################################################################

from mpi4py import MPI
import numpy as np

# Get the number of active tasks in the global communicator

global_comm = MPI.COMM_WORLD
size = global_comm.Get_size()

# Create a new 1D Cartesian communicator of length size. We want periodicity 
# in the one dimension. The 'reorder' parameter is set to True, meaning MPI 
# is allowed to reorder the ranks in the new communicator

comm = global_comm.Create_cart( (size,), periods=(True,), reorder=True)

# Check rank in new communicator and work out neighbouring ranks in 1-d: 
#   my_left - rank - my_right

rank = comm.Get_rank()
my_left, my_right = comm.Shift( 0, 1 )

# Initialise the sum value

sum = 0

# Set the size and datatype for the send and receive message buffers

sendbuf = np.empty( [1], dtype=np.int )
sendbuf[0] = rank
recvbuf = np.empty( [1], dtype=np.int )

# Initialize the requests array

req = [None, None]

for i in range(size):
    req[0] = comm.irecv( source=my_left, tag=9999 )
    req[1] = comm.isend( [sendbuf, MPI.INT], dest=my_right, tag=9999 )

  # Notice the order of the wait calls
    req[1].wait()
    recvbuf = req[0].wait()

    sum += recvbuf[0]
    sendbuf[0] = recvbuf[0]

# Display the result on all ranks, along with the correct answer
print "Rank " + str(rank) + " has sum of ranks " + str(sum) + "; Answer = " + str( (size-1)*size/2 )
