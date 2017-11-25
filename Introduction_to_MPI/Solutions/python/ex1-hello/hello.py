################################################################################## 
#
#   An introductory MPI program using the default communicator
#   MPI_COMM_WORLD to print a message to the screen on each rank.
# 
################################################################################## 

from mpi4py import MPI

rank = MPI.COMM_WORLD.Get_rank()
size = MPI.COMM_WORLD.Get_size()

print "Hello from rank " + str(rank) + " of " + str(size)

