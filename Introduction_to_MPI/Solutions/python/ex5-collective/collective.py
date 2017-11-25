####################################################################################
## Simple script that determines the sum of the IDs of all active MPI tasks using a 
## single global collective call
####################################################################################

from mpi4py import MPI
import numpy as np

# Query the MPI communicator for the number of active MPI tasks and the ID of each 
# task

comm = MPI.COMM_WORLD
rank = comm.Get_rank()
size = comm.Get_size()

# Call the Allreduce global collective to produce the sum of all MPI task ids

data = np.array( int(rank) )
sum = np.zeros( (1,), dtype=np.int )
comm.Allreduce( data, sum, op=MPI.SUM )

# Display the result on all ranks, along with the correct answer

print "Rank " + str(rank) + " has sum of ranks " + str(sum) + "; Answer = " + str( (size-1)*size/2 )

